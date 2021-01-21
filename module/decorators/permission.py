import datetime
from functools import wraps
from rest_framework.response import Response

from database.soccer.models import *
from module.constant.ret_codes import *
from module.constant.constants import *

def token_required(func):
    """Administrator ajax request permission decorator
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = args[1].POST.get('token')
        # if token is not passed
        if not token:
            return Response(RES_ERR_TOKEN_REQUIRED, status=401)

        # if the token is not a registered one
        if len(TBLToken.objects.filter(token=token)) == 0:
            return Response(RES_ERR_INVALID_TOKEN, status=401)

        # if the token is expired
        token = TBLToken.objects.get(token=token)
        cur_time = datetime.datetime.now(datetime.timezone.utc)
        if (cur_time - token.created_time).seconds > TOKEN_LIFE_TIME:
            return Response(RES_ERR_INVALID_TOKEN, status=401)

        return func(*args, **kwargs)

    return decorated_function