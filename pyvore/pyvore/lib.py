import re
import hashlib
import random
import string
import pytz

from pyvore.interfaces import ISession

slugify_strip_re = re.compile(r'[^\w\s-]')
slugify_hyphenate_re = re.compile(r'[-\s]+')

def map_dict_to_obj(data, obj):
    for k, v in data.items():
        setattr(obj, k, v)

def get_session(request):
    session = request.registry.getUtility(ISession)

    return session

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(slugify_strip_re.sub('', value).strip().lower())
    return slugify_hyphenate_re.sub('-', value)

def gen_api_key(length):
    """Generate an api key for the user to use"""
    m = hashlib.sha256()
    word = ''

    for i in xrange(length):
        word += random.choice(string.ascii_letters)

    m.update(word)

    return unicode(m.hexdigest()[:length])

def convert_to_code(num):
    """Converts a decimal id number into a shortened code."""
    # base to convert to (56 for our standard alphabet)
    base = len(string.ascii_letters)
    chars = []

    num += 100

    while num:
        chars.append(string.ascii_letters[num % base])
        num = num / base

    # moved right to left, so reverse order
    chars.reverse()

    return ''.join(chars) # convert stored characters to single string


def resolve_to_id(code):
    """Converts the shortened code back to an id number in decimal form. """
    base = len(string.ascii_letters)
    size = len(code)
    num = -100
    for i in range(0, size): #convert from higher base back to decimal
        num += string.ascii_letters.index(code[i]) * (base ** (size-i-1))
    return num

def utc(dt, str_timezone):
    """Returns dt (datetime.datetime object), converted to UTC from str_timezone."""
    loc_zone = pytz.timezone(str_timezone)
    loc_date = loc_zone.localize(dt)
    return loc_date.astimezone(pytz.utc)

def local(utc_date, str_timezone):
    """Returns localized utc_date, converted from UTC to str_timezone."""
    utc_date = pytz.utc.localize(utc_date)
    loc_tz = pytz.timezone(str_timezone)
    return loc_tz.normalize(utc_date.astimezone(loc_tz))
