from aiogram import Router
from aiogram.filters import Text, CommandStart
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_RU import ANSWERS_LEXICON
other_router: Router = Router()

@other_router.message()
async def process_other_message(message: Message):
    await message.answer(text=ANSWERS_LEXICON['other_message'])

