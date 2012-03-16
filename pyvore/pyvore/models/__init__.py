from sqlalchemy import Column
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import Integer

from pyvore.lib import local

from datetime import datetime
from datetime import date
from datetime import time

import re

# ZopeTransactionExtension hooks up our sessions to a central transaction,
# so that we can rollback even for exceptions that happen outside of the database
DBSession = scoped_session(sessionmaker())

class Base(object):
    """Base class which auto-generates tablename, surrogate
    primary key column.

    Also includes a scoped session and a database generator.
    """
    __table_args__ = {'sqlite_autoincrement': True}


    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase class name to underscores_between_words 
        table name."""
        name = cls.__name__
        return (
            name[0].lower() + 
            re.sub(r'([A-Z])', lambda m:"_" + m.group(0).lower(), name[1:])
        )

    pk =  Column(Integer, primary_key=True, autoincrement=True)

    def _localize_time(self, date_key, time_key, tz):
        _at = datetime.combine(getattr(self,date_key), getattr(self,time_key))
        _at = local(_at, tz)
        return {date_key:_at.date(), time_key:_at.time()}

    def serialize(self, localtz=None):
        """Converts all the properties of the object into a dict
        for use in json
        """
        props = {}

        def is_valid_key(key):
            if not key.startswith('_') and \
               not 'password' in key and \
               not 'salt' == key:
               return True

        _items = self.__class__.__dict__
        local_at = dict()
        if _items.has_key('timezone') and (getattr(self, 'timezone') or localtz):
            timezone = localtz or getattr(self,'timezone')
            if _items.has_key('start_time') and getattr(self,'start_time'):
                local_at.update(self._localize_time('start_date', 'start_time', timezone.name))
            if _items.has_key('end_time') and getattr(self,'end_time'):
                local_at.update(self._localize_time('end_date', 'end_time', timezone.name))

        for key, value in _items.items():
            if is_valid_key(key):
                obj = getattr(self, key)
                if hasattr(obj, 'serialize'):
                    props[key] = obj.serialize()
                elif not callable(obj):
                    if isinstance(obj, datetime) or isinstance(obj, date):
                        _date = local_at.get(key,None) or obj
                        props[key] = _date.strftime("%Y-%m-%d")
                    elif isinstance(obj, time):
                        _time = local_at.get(key,None) or obj
                        props[key] = _time.strftime("%I:%M %p")
                    else:
                        props[key] = getattr(self, key)

        props['id'] = str(self.pk)

        return props

Entity = declarative_base(cls=Base)

def includeme(config):
    config.scan('pyvore.models')
    config.scan('pyvore.models.sessions')
