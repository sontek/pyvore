#!/usr/bin/env python
import os
import sys
import transaction
import json
import datetime
from getpass import getpass
from pyramid.config import Configurator

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from pyramid_signup.models import User
from pyramid_signup.models import SUEntity

from pyvore.models import Entity
from pyvore.models.sessions import Session

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

here = os.path.dirname(__file__)

def usage(argv):# pragma: no cover 
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv): # pragma: no cover
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    config = Configurator(
        settings=settings
    )

    config.include('pyvore.models')

    engine = engine_from_config(settings, 'sqlalchemy.')
    session = DBSession(bind=engine)
    Entity.metadata.bind = engine
    SUEntity.metadata.bind = engine

    Entity.metadata.drop_all(engine)
    SUEntity.metadata.drop_all(engine)

    SUEntity.metadata.create_all(engine)
    Entity.metadata.create_all(engine)

    f = open(os.path.join(here, 'pycon.json')).read()
    data = json.loads(f)
    for d in data:
        title = d['title']
        start = d['start']
        start = datetime.datetime(start[0], start[1], start[2], start[3])

        new_session = Session(title=title, start=start)
        session.add(new_session)

    username = raw_input("What is your username?: ").decode('utf-8')
    email = raw_input("What is your email?: ").decode('utf-8')
    password = getpass("What is your password?: ").decode('utf-8')

    admin = User(username=username, password=password, email=email,
            activated=True)

    session.add(admin)

    transaction.commit()

if __name__ == "__main__": # pragma: no cover
    main()
