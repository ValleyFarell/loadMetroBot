from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.database import users_db
from aiogram.types import CallbackQuery

class IsPersonalKeyFilter(BaseFilter):
    def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and int(message.text) in list(users_db.keys())


class IsYesLinkingCallback(BaseFilter):
    def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'yes_linking' in callback.data and callback.data.split('|')[1].isdigit()

class IsNoLinkingCallback(BaseFilter):
    def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'no_linking' in callback.data and callback.data.split('|')[1].isdigit()

class IsPlayerInGame(BaseFilter):
    def __call__(self, message: Message) -> bool:
        return users_db[message.from_user.id]['in_game']