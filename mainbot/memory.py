from datetime import datetime, timezone
from pathlib import Path


class ObsidianMemory:
    SECTIONS = (
        "Core Profile",
        "Preferences",
        "Goals",
        "Fitness",
        "Trading",
        "Sports",
        "Important Context",
    )

    def __init__(self, vault_path: str | None = None, note_name: str = "Bot Memory.md") -> None:
        default_vault = Path(__file__).resolve().parent.parent
        self._vault_path = Path(vault_path).expanduser() if vault_path else default_vault
        self._note_path = self._vault_path / note_name

    @property
    def note_path(self) -> Path:
        return self._note_path

    def ensure_exists(self) -> None:
        if self._note_path.exists():
            return

        self._note_path.parent.mkdir(parents=True, exist_ok=True)
        self._note_path.write_text(
            "# Bot Memory\n\n"
            "This note is the bot's long-term memory about you.\n\n"
            "Only store information here that you want the bot to remember and use in future replies.\n\n"
            "## Core Profile\n\n"
            "- Name: unknown\n"
            "- Preferred style: practical, conversational, clear\n\n"
            "## Preferences\n\n"
            "## Goals\n\n"
            "## Fitness\n\n"
            "## Trading\n\n"
            "## Sports\n\n"
            "## Important Context\n",
            encoding="utf-8",
        )
        self._ensure_sections()

    def _ensure_sections(self) -> None:
        text = self._note_path.read_text(encoding="utf-8")
        changed = False

        for section in self.SECTIONS:
            heading = f"## {section}"
            if heading not in text:
                if not text.endswith("\n"):
                    text += "\n"
                text += f"\n{heading}\n"
                changed = True

        if changed:
            self._note_path.write_text(text, encoding="utf-8")

    def read_context(self, max_chars: int = 4000) -> str:
        self.ensure_exists()
        self._ensure_sections()
        text = self._note_path.read_text(encoding="utf-8").strip()
        if len(text) <= max_chars:
            return text
        return text[-max_chars:]

    def remember(
        self,
        text: str,
        source: str = "telegram",
        section: str | None = None,
    ) -> None:
        cleaned = " ".join(text.strip().split())
        if not cleaned:
            raise ValueError("memory text cannot be empty")

        self.ensure_exists()
        self._ensure_sections()
        target_section = self._normalize_section(section)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        entry = f"- [{timestamp}] ({source}) {cleaned}"
        self._insert_entry(target_section, entry)

    def clear(self) -> None:
        if self._note_path.exists():
            self._note_path.unlink()
        self.ensure_exists()

    def _normalize_section(self, section: str | None) -> str:
        if not section:
            return "Important Context"

        for known_section in self.SECTIONS:
            if section.lower() == known_section.lower():
                return known_section

        return "Important Context"

    def _insert_entry(self, section: str, entry: str) -> None:
        text = self._note_path.read_text(encoding="utf-8")
        heading = f"## {section}"
        start = text.find(heading)
        if start == -1:
            text = text.rstrip() + f"\n\n{heading}\n\n"
            start = text.find(heading)

        next_start = text.find("\n## ", start + len(heading))
        if next_start == -1:
            section_text = text[start:].rstrip()
            replacement = f"{section_text}\n\n{entry}\n"
            text = text[:start] + replacement
        else:
            section_text = text[start:next_start].rstrip()
            replacement = f"{section_text}\n\n{entry}\n"
            text = text[:start] + replacement + text[next_start:]

        self._note_path.write_text(text, encoding="utf-8")
