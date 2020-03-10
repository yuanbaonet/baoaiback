from app import db
from flask import current_app,request
from app.common.status import Status
from app.common.schema import *
from app.common.param import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from app.common.result import Result
from .model import *
from .schema import *
from .param import *
import random
import string
from sqlalchemy import or_

ns = Namespace("adminroles", description="adminroles API Resource")
