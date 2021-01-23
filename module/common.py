"""common module
"""
import random
import string
from cryptography.fernet import Fernet

def check_payloads(exp_args, payload):
    """Check payload if they are all in right format

    Args:
        exp_args
            List of dictionary which includes field name, and its property
        payload
            Payload of request
    Returns:
        -1: if there is at least one missing field
        -2: if there is at least one invalid field
        0: All are fine
    """
    for arg in exp_args:
        if arg['required'] and arg['field'] not in payload:
            return -1

    for arg in exp_args:
        if arg['field'] not in payload:
            continue
        p = payload[arg['field']]
        if len(p) == 0:
            return -2

        if arg['type'] == 'integer':
            try:
                p = float(p)
                if p != int(p):
                    return -2
                if p < 0:
                    return -2
            except:
                return -2

        elif arg['type'] == 'float':
            try:
                p = float(p)
                if p < 0:
                    return -2
            except:
                return -2

    return 0


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


key = b'GZWKEhHGNopxRdOHS4H4IyKhLQ8lwnyU7vRLrM3sebY='
def encrypt(message: bytes, key: bytes) -> bytes:
    """Fernet encrypt"""
    return Fernet(key).encrypt(message).decode()

def decrypt(token: bytes, key: bytes) -> bytes:
    """Fernet decrypt"""
    return Fernet(key).decrypt(token).decode()


def generate_token(length=70):
    """Generate random token with passed length

    Args:
        length
            Length of token (default: 70)
    Returns:
        Token with specified length
    """
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


def encode_password(password):
    """encode password"""
    return encrypt(password.encode(), key)

def decode_password(password):
    """decode password"""
    return decrypt(password.encode(), key)



