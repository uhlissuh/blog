from string import letters
import hashlib
import random
import hmac

secret = "fdfdf434@!^&*AAAA"


#secure cookie stuff
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#user encryption stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_password_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_password_hash(name, pw, salt)
