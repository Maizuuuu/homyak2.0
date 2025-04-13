from telebot import TeleBot, types
import keyboards as kb
from service import GameService


class CallbackHandler:
    def __init__(self, bot: TeleBot):
        """Создание обработчика колбеков для ввода кода приглашения.

        Args:
            bot (TeleBot): объект бота
        """
        self.bot = bot

        bot.register_callback_query_handler(
            self.handle_invite_code, func=lambda call: call.data == kb.INVITE_CODE
        )
        bot.register_callback_query_handler(
            self.handle_cancel,
            func=lambda call: call.data == kb.CANCLE_INPUT_INVITE_CODE,
        )

    def handle_invite_code(self, call: types.CallbackQuery):
        """Обработчик нажатия на кнопку "Указать код"."""
        self.bot.delete_message(call.message.chat.id, call.message.id)
        self.bot.send_message(
            call.message.chat.id,
            (
                "Укажите пригласительный код, чтобы получить бонус!\n\n"
                "(Пример кода: 123456)"
            ),
            reply_markup=kb.cancle_input_invite_code,
        )
        self.bot.register_next_step_handler(call.message, self.handle_invite_code_input)
        self.bot.answer_callback_query(call.id)

    def handle_cancel(self, call: types.CallbackQuery):
        """Обработчик нажатия на кнопку "Отмена" при вводе кода."""
        self.bot.delete_message(call.message.chat.id, call.message.id)
        self.bot.clear_step_handler_by_chat_id(call.message.chat.id)
        self.bot.send_message(
            call.message.chat.id,
            ("Привет, фармер!" "(тут нужно написать красивый текст)"),
            reply_markup=kb.start_kb,
        )

    def handle_invite_code_input(self, message: types.Message):
        """Обработка ввода пригласительного кода от пользователя."""

        invite_code = message.text.strip()

        try:
            invite_code = int(invite_code)
        except ValueError:
            self.bot.send_message(
                message.chat.id,
                "Код должен состоять только из цифр! Попробуйте еще раз",
            )
            self.bot.register_next_step_handler(message, self.handle_invite_code_input)
            return

        error = GameService().give_startpack(message.from_user, invite_code)

        if error:
            self.bot.send_message(
                message.chat.id,
                error,
            )
            self.bot.register_next_step_handler(message, self.handle_invite_code_input)
            return

        self.bot.send_message(
            message.chat.id, 
            "Код успешно обработан! Вы получаете стартовый бонус в виде 100 коинов!", 
            reply_markup=kb.start_game_kb
        )
