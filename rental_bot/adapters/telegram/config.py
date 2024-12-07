from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramConfig:
    bot_token: str = field(default_factory=lambda: environ["APP_TELEGRAM_BOT_TOKEN"])
    group_id: int = field(default_factory=lambda: int(environ["APP_TELEGRAM_GROUP_ID"]))
