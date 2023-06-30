from aiogram.fsm.state import StatesGroup, State

class game_states(StatesGroup):
    game_with_bot_state = State()
    game_with_friend_state_reg = State()
    game_with_friend_state = State()