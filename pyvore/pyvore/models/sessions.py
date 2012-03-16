from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.types import UnicodeText
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation

from pyramid_signup.models import User
from pyvore.models import Entity
from datetime import datetime

class Session(Entity):
    title = Column(UnicodeText, nullable=False)
    start = Column(DateTime, nullable=False)

class Chat(Entity):
    chat_line = Column(UnicodeText, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    session_pk = Column(Integer, ForeignKey('session.pk'))
    session = relation('Session')
    user_pk = Column(Integer, ForeignKey(User.pk))
    user = relation(User)
