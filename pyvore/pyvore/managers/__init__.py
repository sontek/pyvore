from pyvore.lib import get_session

class BaseManager(object):
    def __init__(self, request):
        self.request = request
        self.session = get_session(request)

