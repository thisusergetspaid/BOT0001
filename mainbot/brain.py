import re
from dataclasses import dataclass

from openai import OpenAI

from domain_tools import DomainTools
from memory import ObsidianMemory
from personality import SYSTEM_PROMPT


@dataclass
class Reply:
    text: str


@dataclass(frozen=True)
class MemoryCandidate:
    text: str
    section: str


class Brain:
    def __init__(
        self,
        api_key: str,
        model: str,
        memory: ObsidianMemory | None = None,
    ) -> None:
        self._client = OpenAI(api_key=api_key) if api_key else None
        self._model = model
        self._history: dict[int, list[dict[str, str]]] = {}
        self._pending_memory: dict[int, MemoryCandidate] = {}
        self._tools = DomainTools()
        self._memory = memory or ObsidianMemory()

    def _history_for(self, chat_id: int) -> list[dict[str, str]]:
        if chat_id not in self._history:
            self._history[chat_id] = []
        return self._history[chat_id]

    def reset(self, chat_id: int) -> None:
        self._history.pop(chat_id, None)

    def remember(
        self,
        text: str,
        source: str = "telegram",
        section: str | None = None,
    ) -> None:
        candidate = self._memory_candidate(text)
        target_section = section or (candidate.section if candidate else "Important Context")
        self._memory.remember(text, source=source, section=target_section)

    def memory_note_path(self) -> str:
        self._memory.ensure_exists()
        return str(self._memory.note_path)

    async def respond(self, chat_id: int, message: str) -> Reply:
        confirmation_reply = self._handle_memory_confirmation(chat_id, message)
        if confirmation_reply:
            return confirmation_reply

        memory_candidate = self._memory_candidate(message)

        tool_result = self._tools.try_answer(message)
        if tool_result:
            history = self._history_for(chat_id)
            history.append({"role": "user", "content": message})
            answer = self._with_memory_prompt(chat_id, tool_result.text, memory_candidate)
            history.append({"role": "assistant", "content": answer})
            return Reply(text=answer)

        if not self._client:
            text = (
                "I can receive messages, but OPENAI_API_KEY is not configured yet.\n"
                "Add it to your .env file, then restart the bot."
            )
            return Reply(text=self._with_memory_prompt(chat_id, text, memory_candidate))

        history = self._history_for(chat_id)
        history.append({"role": "user", "content": message})
        memory_context = self._memory.read_context()

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "system",
                    "content": (
                        "Use this Obsidian memory as personal context when it is relevant. "
                        "Do not mention it unless the user asks about memory.\n\n"
                        f"{memory_context}"
                    ),
                },
                *history[-12:],
            ],
            temperature=0.4,
        )

        answer = response.choices[0].message.content or "I couldn't generate a response."
        answer = self._with_memory_prompt(chat_id, answer, memory_candidate)
        history.append({"role": "assistant", "content": answer})

        return Reply(text=answer)

    def _handle_memory_confirmation(self, chat_id: int, message: str) -> Reply | None:
        pending = self._pending_memory.get(chat_id)
        if not pending:
            return None

        normalized = message.strip().lower()
        yes_words = {"yes", "y", "yeah", "yep", "sure", "remember it", "save it"}
        no_words = {"no", "n", "nope", "dont", "don't", "do not", "forget it"}

        if normalized in yes_words:
            self._memory.remember(pending.text, source="telegram", section=pending.section)
            self._pending_memory.pop(chat_id, None)
            return Reply(text=f"Saved that under {pending.section} in Obsidian memory.")

        if normalized in no_words:
            self._pending_memory.pop(chat_id, None)
            return Reply(text="Got it. I will not save that.")

        return None

    def _with_memory_prompt(
        self,
        chat_id: int,
        answer: str,
        candidate: MemoryCandidate | None,
    ) -> str:
        if not candidate:
            return answer

        self._pending_memory[chat_id] = candidate
        return (
            f"{answer}\n\n"
            "Should I remember this? Reply yes or no.\n"
            f"Memory suggestion: {candidate.section} - {candidate.text}"
        )

    def _memory_candidate(self, message: str) -> MemoryCandidate | None:
        cleaned = " ".join(message.strip().split())
        if len(cleaned) < 12 or cleaned.startswith("/"):
            return None

        lowered = cleaned.lower()
        if "?" in cleaned and not any(phrase in lowered for phrase in ("my name is", "i prefer", "i like")):
            return None

        section_patterns = (
            ("Core Profile", r"\b(my name is|i am \d+|i'm \d+|i live in|i work as|my birthday is)\b"),
            ("Fitness", r"\b(my weight|i weigh|my height|bulk|cut|maintenance|workout|training|gym|calories|protein|diet)\b"),
            ("Trading", r"\b(my watchlist|i trade|trading|stocks|options|crypto|forex|risk tolerance|portfolio)\b"),
            ("Sports", r"\b(my team|favorite team|i follow|nba|nfl|mlb|nhl|ufc|soccer|betting)\b"),
            ("Preferences", r"\b(i prefer|i like|i love|i hate|i don't like|i do not like|my favorite|i usually|i want you to)\b"),
            ("Goals", r"\b(my goal is|my goals are|i want to|i'm trying to|i am trying to|i plan to|i'm working on)\b"),
        )

        for section, pattern in section_patterns:
            if re.search(pattern, lowered):
                return MemoryCandidate(text=cleaned, section=section)

        if re.search(r"\b(i am|i'm|my|me)\b", lowered):
            return MemoryCandidate(text=cleaned, section="Important Context")

        return None
