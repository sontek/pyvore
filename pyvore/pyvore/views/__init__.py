from pyramid.view import view_config
from pyramid.response import Response

from pyvore.lib import get_session
from pyvore.models.sessions import Chat
from pyvore.models import DBSession

from socketio import socketio_manage

from json import dumps
from json import loads

from socketio.namespace import BaseNamespace

import redis

class BaseController(object):
    @property
    def request(self):
        # we defined this so that we can override the request in tests easily
        return self._request

    def __init__(self, request):
        self._request  = request

        self.settings = request.registry.settings
        self.db = get_session(request)

@view_config(route_name='index', renderer='base.jinja2')
def index(request):
    return {}


class ChatNamespace(BaseNamespace):
    def listener(self, channel):
        r = redis.StrictRedis()
        r = r.pubsub()

        # only subscribe to the channel we are currently in
        r.subscribe('chat:' + channel)

        for m in r.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                self.emit("chat", data)

    def on_chat(self, msg_id, msg):
        """Called by client-side: chat.emit("chat", {"foo": "bar"});"""
        r = redis.Redis()
        chat_line = msg

        chat = Chat(chat_line=chat_line,
            user_pk=self.request.user.pk,
            session_pk=int(msg_id)
        )

        DBSession.add(chat)
        DBSession.commit()

        # only publish to the channel the message came from
        r.publish('chat:' + msg_id, dumps(chat.serialize()))

    def on_subscribe(self, channel):
        self.spawn(self.listener, channel['id'])


@view_config(route_name='socket_io')
def socketio_service(request):
    retval = socketio_manage(request.environ,
        {
            '/chat': ChatNamespace,
        }, request=request
    )

    return Response(retval)
