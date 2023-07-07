from aiogram import Router
from aiogram.filters import Text, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import create_menu_kb
from lexicon.lexicon_RU import ANSWERS_LEXICON
from states.states import game_states
from database.database import users_db
other_router: Router = Router()

@other_router.message(game_states.game_with_friend_state_reg)
async def process_wrong_personal_key(message: Message):
    await message.answer(text=ANSWERS_LEXICON['wrong_personal_key'], reply_markup=create_menu_kb(1))
@other_router.message()
async def process_other_message(message: Message):
    await message.answer(text=ANSWERS_LEXICON['other_message'])

@other_router.callback_query()
async def process_other_callback(callback: CallbackQuery):
    print(callback.data)
