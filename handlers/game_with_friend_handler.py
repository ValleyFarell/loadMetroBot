from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config.config import Config, load_config
from lexicon.lexicon_RU import ANSWERS_LEXICON, GAME_BUTTONS, LEXICON_BUTTONS, MOVES
from filters.game_with_friend_filters import IsPersonalKeyFilter, IsPlayerInGame
from aiogram.filters import and_f, StateFilter
from services.data_reset import data_reset
from states.states import game_states
from database.database import users_db
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import create_linking_kb, game_kb, create_menu_kb
from aiogram.filters import Text
from services.game_mechanics import spot_winner
game_with_friend_router: Router = Router()

@game_with_friend_router.message(StateFilter(game_states.game_with_friend_state_reg), lambda x: x.text.isdigit() and int(x.text) in list(users_db.keys()))
async def process_game_reg(message: Message, state: FSMContext):
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    if users_db[int(message.text)]['is_wait_game']:
        await bot.send_message(chat_id=int(message.text), text=ANSWERS_LEXICON['linking_text'].format(message.from_user.id), reply_markup=create_linking_kb(2, message.from_user.id))
        await state.clear()
    else:
        await message.answer(text=ANSWERS_LEXICON['no_friend_answer'])
        await message.answer(text=LEXICON_BUTTONS['menu'], reply_markup=create_menu_kb(2))
        await state.clear()

@game_with_friend_router.callback_query(Text(startswith='yes'))
async def process_play_with_bot_command(callback: CallbackQuery, state: FSMContext):
    friend_id = int(callback.data.split('|')[1])
    users_db[friend_id]['friend_id'] = callback.from_user.id
    users_db[callback.from_user.id]['friend_id'] = friend_id
    users_db[callback.from_user.id]['in_game'] = True
    users_db[users_db[callback.from_user.id]['friend_id']]['in_game'] = True
    users_db[callback.from_user.id]['is_wait_game'] = False
    users_db[users_db[callback.from_user.id]['friend_id']]['is_wait_game'] = False
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await bot.send_message(chat_id=friend_id, text=GAME_BUTTONS['user_move'], reply_markup=game_kb)
    await callback.message.answer(text=GAME_BUTTONS['user_move'], reply_markup=game_kb)
    await state.set_state(game_states.game_with_friend_state)

@game_with_friend_router.callback_query(Text(startswith='no'))
async def process_play_with_bot_command(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['is_wait_game'] = False
    users_db[users_db[callback.from_user.id]['friend_id']]['is_wait_game'] = False
    friend_id = int(callback.data.split('|')[1])
    await callback.message.edit_text(text=LEXICON_BUTTONS['menu'], reply_markup=create_menu_kb(2))
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await bot.send_message(chat_id=friend_id, text=ANSWERS_LEXICON['no_friend_answer'], reply_markup=create_menu_kb(2))
    data_reset(callback.from_user.id)
    data_reset(users_db[callback.from_user.id]['friend_id'])
    await state.clear()


@game_with_friend_router.message(Text(text=['📜', '✂️', '🗿']), lambda x: users_db[x.from_user.id]['in_game'])
async def process_game(message: Message, state: FSMContext):
    users_db[message.from_user.id]['is_moved'] = True
    users_db[message.from_user.id]['move'] = message.text
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    if users_db[users_db[message.from_user.id]['friend_id']]['is_moved']:
        await message.answer(text=users_db[users_db[message.from_user.id]['friend_id']]['move'])
        await bot.send_message(users_db[message.from_user.id]['friend_id'], text=message.text)
        user_move = users_db[message.from_user.id]['move']
        friend_move = users_db[users_db[message.from_user.id]['friend_id']]['move']
        game_result = spot_winner(user_move, friend_move)
        if game_result == 'w':
            users_db[message.from_user.id]['score'] += 1
        elif game_result == 'l':
            users_db[users_db[message.from_user.id]['friend_id']]['score'] += 1
        await message.answer(text=ANSWERS_LEXICON['friend_game_result'].format(users_db[message.from_user.id]['score'],
                                                                        users_db[users_db[message.from_user.id]['friend_id']]['score']),
                                                                        reply_markup=game_kb)
        await bot.send_message(users_db[message.from_user.id]['friend_id'], text=ANSWERS_LEXICON['friend_game_result'].format(users_db[users_db[message.from_user.id]['friend_id']]['score'],
                                                                        users_db[message.from_user.id]['score']), reply_markup=game_kb)
        users_db[message.from_user.id]['is_moved'] = False
        users_db[users_db[message.from_user.id]['friend_id']]['is_moved'] = False
    else:
        return None


@game_with_friend_router.message(Text(text='Выйти'), lambda x: users_db[x.from_user.id]['in_game'])
async def process_game(message: Message, state: FSMContext):
    users_db[message.from_user.id]['in_game'] = False
    users_db[users_db[message.from_user.id]['friend_id']]['in_game'] = False
    users_db[message.from_user.id]['in_game'] = False
    users_db[users_db[message.from_user.id]['friend_id']]['in_game'] = False
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await message.answer(text=ANSWERS_LEXICON['friend_game_final_result'].format(users_db[message.from_user.id]['score'],
                                                                        users_db[users_db[message.from_user.id]['friend_id']]['score']),
                                                                        reply_markup=ReplyKeyboardRemove())
    await bot.send_message(users_db[message.from_user.id]['friend_id'], text=ANSWERS_LEXICON['friend_game_final_result'].format(users_db[users_db[message.from_user.id]['friend_id']]['score'],
                                                                        users_db[message.from_user.id]['score']), reply_markup=game_kb)
    await bot.send_message(users_db[message.from_user.id]['friend_id'], text=LEXICON_BUTTONS['menu'], reply_markup=create_menu_kb(2))
    await message.answer(text=LEXICON_BUTTONS['menu'], reply_markup=create_menu_kb(2))
    data_reset(message.from_user.id)
    data_reset(users_db[message.from_user.id]['friend_id'])
    await state.clear()





        
