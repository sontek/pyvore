from pyvore.managers import BaseManager
from pyvore.models.sessions import Session
from pyvore.models.sessions import Chat

class SessionManager(BaseManager):
    def get_sessions(self):
        return self.session.query(Session).all()

    def get_chatlog(self, pk):
        return self.session.query(Chat).filter(Chat.session_pk == pk)
