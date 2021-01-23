from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('login', Login, 'auth-login')
    router.register('signup', Signup, 'auth-signup')






