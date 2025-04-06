from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

INVITE_CODE = "invite_code"
START_GAME = "start_game"
CANCLE_INPUT_INVITE_CODE = "cancle_input_invite_code"
UPGRADE_LEVEL = "upgrade_level"
FRIENDS_LIST = "friends_list"
UPDATE_INFO = "update_info"
BACK_TO_MAIN = "back_to_main"

start_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Указать код", callback_data=INVITE_CODE),
    InlineKeyboardButton("Начать игру!", callback_data=START_GAME),
)

cancle_input_invite_code = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Отмена", callback_data=CANCLE_INPUT_INVITE_CODE)
)

start_game_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Начать игру!", callback_data=START_GAME)
)

game_kb_main = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Обновить", callback_data=UPDATE_INFO),
    InlineKeyboardButton("Прокачать уровень", callback_data=UPGRADE_LEVEL),
    InlineKeyboardButton("Список друзей", callback_data=FRIENDS_LIST),
)

game_kb_back_to_main = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Назад", callback_data=BACK_TO_MAIN),
)
