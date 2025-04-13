from telebot import TeleBot, types, apihelper
import keyboards as kb
from models import User
from service import GameService


class CallbackHandler:
    MAIN_TEXT = (
        "Ваши коины: {coins}\n\n"
        "Текущий доход коинов в 10 секунд: {level}\n"
        "Пассивный доход от друзей: {invited}\n\n"
        "[Стоимость следующего уровня: {price}]"
    )

    def __init__(self, bot: TeleBot):
        """Создание обработчика колбеков для основного функционала игры.

        Args:
            bot (TeleBot): объект бота
        """
        self.bot = bot

        bot.register_callback_query_handler(
            self.handle_main_menu, func=lambda call: call.data == kb.START_GAME)
        
        bot.register_callback_query_handler(
            self.handle_update_info, func=lambda call: call.data == kb.UPDATE_INFO)
        
        bot.register_callback_query_handler(
            self.handle_friends_list, func=lambda call: call.data == kb.FRIENDS_LIST)
        
        bot.register_callback_query_handler(
            self.handle_back_to_main, func=lambda call: call.data == kb.BACK_TO_MAIN)
        
        bot.register_callback_query_handler(
            self.handle_upgrade_level, func=lambda call: call.data == kb.UPGRADE_LEVEL)
        # TODO: описать функцию
        ...

    def handle_main_menu(self, call: types.CallbackQuery):
        """Обработка главного игрового меню."""
        self.bot.answer_callback_query(call.id)
        self.bot.delete_message(call.message.chat.id, call.message.id)

        user = GameService().get_user(call.from_user)
        
        invited_users = GameService().get_friends_list(call.from_user)

        levels = []
        for i in invited_users:
            levels.append(i.level)
        passive_income = sum(levels) / 4

        self.bot.send_message(
            call.message.chat.id, self.MAIN_TEXT.format(coins= user.balance,level= user.level,invited= passive_income,price= user.level**2),
            reply_markup=kb.game_kb_main
        )

    def handle_update_info(self, call: types.CallbackQuery):
        """Обработка кнопки "обновить", которая редактирует главное меню, актуализируя данные."""
        self.bot.answer_callback_query(call.id)

        user = GameService().get_user(call.from_user)

        invited_users = GameService().get_friends_list(call.from_user)
        levels = []
        for i in invited_users:
            levels.append(i.level)
        passive_income = sum(levels) / 4

        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,message_id=call.message.id, text=self.MAIN_TEXT.format(coins= user.balance,level= user.level,invited= passive_income,price= user.level**2),
                reply_markup=kb.game_kb_main
            )
        except apihelper.ApiTelegramException as e:
            pass

    def handle_friends_list(self, call: types.CallbackQuery):
        """Отображение списка друзей и пригласительного года при нажатии на кнопку "список друзей"."""
        friends = GameService().get_friends_list(call.from_user)
        text = "You haven't invited any friends!"
        if friends:
            text = 'Your friends:'
            for player in friends:
                text += f"@{player.telegram_name} [LVL {player.level}]\n"
        text += f"\n\n[Your inviter code: {call.from_user.id}]"

        self.bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=kb.game_kb_back_to_main)
        # TODO: описать функцию
        ...

    def handle_back_to_main(self, call: types.CallbackQuery):
        """Возвращает пользователя в главное меню при нажатии кнопки "назад" в списке друзей."""
        self.handle_main_menu(call)
        self.bot.answer_callback_query(call.id)

        # TODO: описать функцию
        ...

    def handle_upgrade_level(self, call: types.CallbackQuery):
        """Обработка улучшения уровня на кпноку "повысить уровень"."""
        upgraded = GameService().upgrade_level(call.from_user)
        if not upgraded:
            self.bot.answer_callback_query(call.id, "Influent ammount of coins!")
            return
        self.bot.answer_callback_query(call.id, "Level-up!")
        # TODO: описать функцию
        ...
