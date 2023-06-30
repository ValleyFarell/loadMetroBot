from aiogram import Bot, Router
from copy import deepcopy
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from config.config import Config, load_config
from lexicon.lexicon_RU import ANSWERS_LEXICON, LEXICON_BUTTONS, MARKUPS_LEXICON, GAME_BUTTONS
from aiogram.types import FSInputFile
from keyboards.keyboards import create_navigation_kb, create_menu_kb, game_kb
from states.states import game_states
from aiogram.fsm.context import FSMContext
from handlers import game_with_bot_handler
from handlers import game_with_friend_handler
from filters.game_with_friend_filters import IsYesLinkingCallback, IsNoLinkingCallback
from database.database import users_db, user_template
from services.data_reset import data_reset
main_router: Router = Router()
main_router.include_router(game_with_bot_handler.game_with_bot_router)
main_router.include_router(game_with_friend_handler.game_with_friend_router)

@main_router.message(CommandStart())
async def process_start_command(message: Message):
    users_base_file = open('database/base.txt', 'r+')
    users_base = users_base_file.read().split(',')
    if str(message.from_user.id) not in users_base:
        users_base_file.write(',' + str(message.from_user.id))
    users_db[message.from_user.id] = deepcopy(user_template)
    data_reset(message.from_user.id)
    photo = FSInputFile('media/photos/start.jpg')
    await message.answer_photo(photo=photo, 
                               caption=ANSWERS_LEXICON['start'], 
                               reply_markup=create_navigation_kb(width=2))

@main_router.callback_query(Text(text='menu'))
async def process_menu_command(callback: CallbackQuery):
    data_reset(callback.from_user.id)
    if callback.message.text:
        await callback.message.edit_text(text=MARKUPS_LEXICON['menu'], reply_markup=create_menu_kb(width=2))
    else:
        await callback.message.answer(text=MARKUPS_LEXICON['menu'], reply_markup=create_menu_kb(width=2))
        await callback.message.delete()
    await callback.answer()

@main_router.callback_query(Text(text='info'))
async def process_menu_command(callback: CallbackQuery):
    if callback.message.text:
        await callback.message.edit_text(text=ANSWERS_LEXICON['info'], reply_markup=create_navigation_kb(width=2, info_visible=False))
    else:
        await callback.message.answer(text=ANSWERS_LEXICON['info'], reply_markup=create_navigation_kb(width=2, info_visible=False))
        await callback.message.delete()
    await callback.answer()

@main_router.callback_query(Text(text='bot_game'))
async def process_play_with_bot_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=GAME_BUTTONS['user_move'], reply_markup=game_kb)
    await state.set_state(game_states.game_with_bot_state)
    await callback.message.delete()

@main_router.callback_query(Text(text='friend_game'))
async def process_play_with_bot_command(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['is_wait_game'] = True
    await callback.message.answer(text=ANSWERS_LEXICON['game_reg'].format(callback.from_user.id), reply_markup=create_navigation_kb(1, info_visible=False))
    await callback.message.delete()
    await state.set_state(game_states.game_with_friend_state_reg)







