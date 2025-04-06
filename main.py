from telebot import TeleBot, types
import schedule
from threading import Thread
import time
import config
import keyboards as kb
from service import GameService
from handlers import invite_code, game
from database import create_all_table

import models  # это нужно, чтобы класс User создался и добавилсяв BaseModel.metadata

# TODO: создать таблиц в БД
create_all_table()

bot = TeleBot(config.TOKEN)
# TODO: создать объекта бота


def schedule_pending():
    """Запуск schedule для обновления коинов каждые 10 секунд.
    В этом потоке запускается функция update_coins из GameService, которая обновляет коинов у всех пользователей.
    """
    schedule.every(10).seconds.do(GameService.update_coins)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # TODO: описать функцию
    ...


@bot.message_handler(commands=["start"])
def handle_start(message: types.Message):
    # TODO: описать функцию
    reg:bool = GameService().check_user_or_register(message.from_user) 
    if not reg:
        bot.send_message(message.chat.id, "Welcome back!", reply_markup=kb.start_game_kb)
        return
    bot.send_message(message.chat.id, ("Hi, gamer!"), reply_markup=kb.start_kb)




# обработка пригласительного кода
# TODO: создать объект обработчика пригласительного кода
invite_code.CallbackHandler(bot)

# основные обработчики игры
# TODO: создать объект обработчика игры
game.CallbackHandler(bot)


# запуск потока для обновления коинов
Thread(target=schedule_pending).start()

print("Бот запущен")
bot.infinity_polling()
