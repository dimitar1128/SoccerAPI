from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('my_team', TeamOwner, 'my-team')
    router.register('team', Team, 'team')






