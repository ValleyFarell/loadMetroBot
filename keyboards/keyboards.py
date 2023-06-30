from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon_RU import LEXICON_BUTTONS, GAME_BUTTONS, ANSWERS_LEXICON

MENU_BUTTON: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_BUTTONS['menu'], callback_data='menu')

INFO_BUTTON: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_BUTTONS['info'], callback_data='info')

PLAY_WITH_BOT_BUTTON: InlineKeyboardButton = InlineKeyboardButton(
    text=GAME_BUTTONS['bot_game'],
    callback_data='bot_game'
)

PLAY_WITH_FRIEND_BUTTON: InlineKeyboardButton = InlineKeyboardButton(
    text=GAME_BUTTONS['friend_game'],
    callback_data='friend_game'
)

game_button1: KeyboardButton = KeyboardButton(text=GAME_BUTTONS['rock'])
game_button2: KeyboardButton = KeyboardButton(text=GAME_BUTTONS['scissors'])
game_button3: KeyboardButton = KeyboardButton(text=GAME_BUTTONS['paper'])
exit_button: KeyboardButton = KeyboardButton(text='Выйти')
game_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
game_kb_builder.row(game_button1, game_button2, game_button3, exit_button, width=1)
game_kb: ReplyKeyboardMarkup = game_kb_builder.as_markup(resize_keyboard=True)


def create_linking_kb(width: int, user_id: int) -> InlineKeyboardMarkup:
    yes_linking_button: InlineKeyboardButton = InlineKeyboardButton(text=ANSWERS_LEXICON['yes_linking'], callback_data='yes_linking' + '|' + str(user_id))
    no_linking_button: InlineKeyboardButton = InlineKeyboardButton(text=ANSWERS_LEXICON['no_linking'], callback_data='yes_linking' + '|' + str(user_id))
    linking_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    linking_kb_builder.row(yes_linking_button, no_linking_button, width=width)
    linking_kb: ReplyKeyboardMarkup = linking_kb_builder.as_markup()
    return linking_kb

def create_navigation_kb(width: int, info_visible: bool = True) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [MENU_BUTTON]
    if info_visible: buttons.append(INFO_BUTTON)
    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()

def create_menu_kb(width: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [PLAY_WITH_FRIEND_BUTTON, PLAY_WITH_BOT_BUTTON, INFO_BUTTON]
    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()



