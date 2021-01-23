from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('market', Market, 'market')