from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('member', Member, 'member')