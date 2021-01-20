"""user module
"""
import logging
from database.soccer.models import *

def get_user_with_token(token):
    """Get user object with token

    Args:
        token
    Returns:
        - when success
            User object
        - when fail
            None
    """
    try:
        token_obj = TBLToken.objects.get(token=token)
        user_obj = TBLUser.objects.get(id=token_obj.user_id)
        return user_obj

    except Exception as e:
        logging.error(str(e))
        return None