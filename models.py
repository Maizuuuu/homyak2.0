from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import BaseModel


class User(BaseModel):
    """Модель пользователя:
    - id (int): id пользователя
    - telegram_name (str): имя пользователя в телеграме
    - telegram_id (int): id пользователя в телеграме, уникальный
    - level (int): уровень пользователя, по умолчанию 1
    - balance (float): баланс пользователя, по умолчанию 0
    - inviter_id (int): id пригласившего пользователя, по умолчанию None
    """
    # TODO: описать модель
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_name = Column(String)
    telegram_id = Column(Integer, unique = True)
    level = Column(Integer, default=1)
    balance = Column(Float, default = 0)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable = True)
