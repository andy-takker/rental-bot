from aiogram import Bot
from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide

from rental_bot.adapters.telegram.bot import make_bot
from rental_bot.adapters.telegram.config import TelegramConfig
from rental_bot.adapters.telegram.sender import TelegramSender
from rental_bot.domains.interfaces.sender import IAdvertSender


class TelegramProvider(Provider):
    def __init__(
        self,
        config: TelegramConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ):
        super().__init__(scope, component)
        self.__config = config

    @provide(scope=Scope.APP)
    def bot(self) -> Bot:
        return make_bot(token=self.__config.bot_token)

    @provide(scope=Scope.APP)
    def sender(self, bot: Bot) -> AnyOf[TelegramSender, IAdvertSender]:
        return TelegramSender(bot=bot, group_id=self.__config.group_id)
