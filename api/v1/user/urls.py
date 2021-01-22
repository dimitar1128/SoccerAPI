from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('user', User, 'user')