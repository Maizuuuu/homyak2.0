from sqlalchemy import func
from sqlalchemy.orm import aliased
from telebot import types
from models import User
from database import create_session


class GameService:
    """Сервис для работы с пользователями и их данными в БД."""

    def __init__(self):
        """Создание сессии для работы с БД при инициализации класса."""
        # TODO: дописать функцию
        self.session = create_session()

    def get_user(self, tg_user: types.User) -> User | None:
        """Получение пользователя из БД по его telegram ID.

        Args:
            tg_user (types.User): Пользователь, который взаимодействует с ботом.

        Returns:
            User | None: Пользователь, если он существует в БД, иначе None.
        """
        # TODO: описать функцию
        user = self.session.query(User).filter(User.telegram_id == tg_user.id).first()
        return user

    def get_friends_list(self, tg_user: types.User) -> list[User]:
        """Получение списка приглашенных пользователей по telegram ID.

        Args:
            tg_user (types.User): Пользователь, который взаимодействует с ботом.

        Returns:
            list[User]: Список пользователей, приглашенных текущим пользователем.
        """
        users = self.session.query(User).filter(User.inviter_id == tg_user.id).all()
        # TODO: описать функцию
        ...
        return users

    def check_user_or_register(self, tg_user: types.User) -> bool:
        """Проверка, существует ли пользователь в БД, если нет - регистрация нового пользователя.

        Args:
            tg_user (types.User): Пользователь, который взаимодействует с ботом.

        Returns:
            bool: True, если пользователь был зарегистрирован, False, если он уже существует.
        """
        # TODO: описать функцию
        user = self.get_user(tg_user)
        if not user:
            new_user = User(telegram_name=tg_user.username, telegram_id=tg_user.id)
            self.session.add(new_user)
            self.session.commit()
            return True
        return False

    def upgrade_level(self, tg_user: types.User) -> bool:
        """Улучшения уровня пользователя, если у него достаточно коинов.
           Стоимость следующего уровня равна квадрату текущего уровня.

        Args:
            tg_user (types.User): Пользователь, который взаимодействует с ботом.

        Returns:
            bool: True, если уровень был успешно улучшен, False, если недостаточно коинов.
        """
        user = self.get_user(tg_user)
        upgrade_need = round(user.level**2 - len(GameService().get_friends_list(user))*user.level)
        if user.balance < upgrade_need:
            return False
        user.balance -= upgrade_need
        user.level += 1
        self.session.commit()
        return True

    def give_startpack(self, tg_user: types.User, invite_code: int) -> str | None:
        """Выдача стартового пакета пользователю, который ввел код приглашения:
        - Если код совпадает с ID пользователя, то выдача не производится.
        - Если код не найден, то выдача также не производится.
        - Если пользователь уже получал стартовый пакет, то выдача также не производится.
        - Если все условия выполнены, то пользователю добавляется 100 коинов и ID пригласившего его пользователя сохраняется в inviter_id.

        Args:
            tg_user (types.User): Пользователь, который взаимодействует с ботом.
            invite_code (int): Код приглашения, который ввел пользователь.

        Returns:
            str | None: Сообщение об ошибке, если код невалидный или пользователь уже получал стартовый пакет, иначе None.
        """
        # TODO: описать функцию
        user = self.get_user(tg_user)

        if invite_code == tg_user.id:
            return "Invalid code: Cannot import your own code!"
        inviter = (
            self.session.query(User).filter(User.telegram_id == invite_code).first()
        )
        if not inviter:
            return "Invalid code: No inviter found!"
        if user.inviter_id:
            return "Invalid code: Code has already used!"
        user.balance += 100
        user.inviter_id = invite_code
        self.session.commit()
        return None

    @staticmethod
    def update_coins():
        """Обновление коинов пользователей в БД. К текущему балансу добавляется:
        - уровень пользователя
        - 1/4 от суммы уровней всех пользователей, которых пригласил текущий пользователь.
        """

        # TODO: описать функцию

        # здесь нужно создавать отдельную сессию
        # т.к. эта функция запускается 1 раз в 10 секунд в другом потоке.
        session = create_session()
        print("Updating coins...")

        Players = aliased(User)
        session.query(User).update(
            {
                User.balance: User.balance
                + User.level
                + session.query(func.coalesce(func.sum(Players.level), 0) / 4)
                .filter(Players.inviter_id == User.telegram_id)
                .scalar_subquery()
            }
        )
        session.commit()