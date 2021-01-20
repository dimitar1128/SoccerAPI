from rbasis.urlrouter import router
from .controllers import *

def RegPath():
    router.register('team/my_team', TeamOwner, 'my-team')






