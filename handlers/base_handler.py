import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps


class BaseHandler(tornado.web.RequestHandler):
    pass
