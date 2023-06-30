from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from lexicon.lexicon_RU import LEXICON_BUTTONS, GAME_BUTTONS, ANSWERS_LEXICON
from states.states import game_states
from services.game_mechanics import spot_winner, get_bot_move
from database.database import users_db
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import game_kb, create_menu_kb
game_with_bot_router: Router = Router()

@game_with_bot_router.message(Text(text=[GAME_BUTTONS['rock'], GAME_BUTTONS['scissors'], GAME_BUTTONS['paper']]), game_states.game_with_bot_state)
async def process_user_move(message: Message, state: FSMContext):
    bot_move: str = get_bot_move()
    user_move: str = message.text
    game_result = spot_winner(user_move, bot_move)
    if game_result == 'w':
        users_db[message.from_user.id]['score'] += 1
    elif game_result == 'l':
        users_db[message.from_user.id]['bot_score'] += 1
    await message.answer(text=bot_move)
    await message.answer(text=ANSWERS_LEXICON['bot_game_result'].format(users_db[message.from_user.id]['bot_score'],
                                                                        users_db[message.from_user.id]['score']),
                                                                        reply_markup=game_kb)
@game_with_bot_router.message(Text(text='Выйти'), game_states.game_with_bot_state)
async def process_exit_game(message: Message, state: FSMContext):
    state.clear()
    clean_markup = ReplyKeyboardRemove()
    await message.answer(text=ANSWERS_LEXICON['bot_game_final_result'].format(users_db[message.from_user.id]['bot_score'],
                                                                        users_db[message.from_user.id]['score']),
                                                                        reply_markup=ReplyKeyboardRemove())
    await message.answer(text=LEXICON_BUTTONS['menu'].format(users_db[message.from_user.id]['bot_score'],
                                                                        users_db[message.from_user.id]['score']),
                                                                        reply_markup=create_menu_kb(2))
    users_db[message.from_user.id]['score'] = 0
