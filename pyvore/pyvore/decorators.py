from pyvore.httpexceptions import HTTPInternalServerError
from pyvore.httpexceptions import HTTPUnauthorized

import traceback
import inspect

def be_json_damnit(fn, *args):
    try:
        result = fn(*args)
        return result
    except Exception as e:
        for line in traceback.format_stack():
            print line.strip()
        frm = inspect.trace()[-1]
        f = inspect.getfile(frm[0])
        lineno = inspect.getlineno(frm[0])

        return HTTPInternalServerError({
            'extras': e.message,
            'details': '%s:%s' % (f, lineno)
        })

def json_result(fn):
    def wrapped(*args):
        return be_json_damnit(fn, *args)

    return wrapped

def secure_json_result(fn):
    def wrapped(*args):
        if args[0].request:
            return be_json_damnit(fn, *args)
        else:
            return HTTPUnauthorized({
                'error': 'You must be logged in'
            })

    return wrapped
