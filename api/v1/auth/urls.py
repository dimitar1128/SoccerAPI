from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('auth/login', Login, 'auth-login')
    router.register('auth/signup', Signup, 'auth-signup')






