import logging
from module.constant.ret_codes import *
from rest_framework import viewsets
from rest_framework.response import Response

from database.soccer.models import *
from module.common import *
from module.constant.constants import *
from module.decorators.permission import *