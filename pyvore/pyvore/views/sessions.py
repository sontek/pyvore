from pyvore.decorators import json_result
from pyvore.views import BaseController
from pyvore.managers.sessions import SessionManager

class SessionController(BaseController):
    def __init__(self, request):
        super(SessionController, self).__init__(request)

        self.mgr = SessionManager(request)

    @json_result
    def get_sessions(self):
        return [t.serialize() for t in self.mgr.get_sessions()]

    @json_result
    def get_chatlog(self):
        pk = self.request.matchdict.get('pk')
        return [t.serialize() for t in self.mgr.get_chatlog(pk)]
