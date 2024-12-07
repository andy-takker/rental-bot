from dataclasses import dataclass, field

from rental_bot.adapters.database.config import DatabaseConfig
from rental_bot.adapters.telegram.config import TelegramConfig


@dataclass(frozen=True, slots=True, kw_only=True)
class ParserConfig:
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
