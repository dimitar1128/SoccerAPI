"""common module
"""
import random
import string

def check_arguments(exp_args, payload):
    """Check arguments if they are all exists in the payload

    Args:
        exp_args
            Expected arguments list
        payload
            Payload of request
    Returns:
        True if all expected arguments are in the payload
        False if at last one expected arguments is not in the payload
    """
    for arg in exp_args:
        if arg not in payload:
            return False

    return True


def generate_token(length=70):
    """Generate random token with passed length

    Args:
        length
            Length of token (default: 70)
    Returns:
        Token with specified length
    """
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

