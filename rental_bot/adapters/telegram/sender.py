from aiogram import Bot
from aiogram.types import InputMediaPhoto

from rental_bot.domains.entities.bpru import Advert
from rental_bot.domains.interfaces.sender import IAdvertSender


class TelegramSender(IAdvertSender):
    def __init__(self, bot: Bot, group_id: int) -> None:
        self.__bot = bot
        self.__group_id = group_id

    async def send_advert(self, advert: Advert) -> None:
        await self.__bot.send_media_group(
            chat_id=self.__group_id,
            media=[InputMediaPhoto(media=str(image)) for image in advert.images],
        )
        await self.__bot.send_message(
            chat_id=self.__group_id,
            text=advert.to_message(),
        )
