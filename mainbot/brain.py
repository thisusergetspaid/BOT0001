from dataclasses import dataclass

from openai import OpenAI

from personality import SYSTEM_PROMPT


@dataclass
class Reply:
    text: str


class Brain:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key) if api_key else None
        self._model = model
        self._history: dict[int, list[dict[str, str]]] = {}

    def _history_for(self, chat_id: int) -> list[dict[str, str]]:
        if chat_id not in self._history:
            self._history[chat_id] = []
        return self._history[chat_id]

    def reset(self, chat_id: int) -> None:
        self._history.pop(chat_id, None)

    async def respond(self, chat_id: int, message: str) -> Reply:
        if not self._client:
            return Reply(
                text=(
                    "I can receive messages, but OPENAI_API_KEY is not configured yet.\n"
                    "Add it to your .env file, then restart the bot."
                )
            )

        history = self._history_for(chat_id)
        history.append({"role": "user", "content": message})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history[-12:]],
            temperature=0.4,
        )

        answer = response.choices[0].message.content or "I couldn't generate a response."
        history.append({"role": "assistant", "content": answer})

        return Reply(text=answer)
