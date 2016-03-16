import tornado.ioloop
import tornado.web
import tornado.escape
import unittest
import time
import signal
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import rethinkdb as r
from tornado.options import define, options
from tornado.web import Application
from config.routes import routes
from modules.linechart_module import LineChartModule
from modules.fcq_card_module import FcqCardModule
from models.fcq import Fcq
from models.grade import Grade
from models.course import Course
from models.instructor import Instructor
from models.department import Department
import logging

settings = {
    'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'static/',
    'login_url': '/login',
    'grade': Grade(),
    'fcq': Fcq(),
    'course': Course(),
    'instructor': Instructor(),
    'department': Department(),
    'ui_modules': {
        'chart_overtime': LineChartModule,
        'fcq_card': FcqCardModule
    }
}


def initialize_settings():
    settings['debug'] = options.debug
    settings['site_port'] = options.port
    database_name = options.database_name
    database_port = options.database_port
    database_host = options.database_host
    if options.debug:
        database_name += '_debug'
    if options.test:
        database_name += '_test'
    settings['database_name'] = database_name
    try:
        conn = r.connect(host=options.database_host, port=options.database_port)
        settings['conn'] = conn
        r.db_create(database_name).run(conn)
    except Exception as e:
        logging.warn(e.message)
    settings['fcq'].init(database_name, conn)
    settings['grade'].init(database_name, conn)
    settings['course'].init(database_name, conn)
    settings['instructor'].init(database_name, conn)
    settings['department'].init(database_name, conn)
    return settings


def make_application(settings):
    return Application(handlers=routes, **settings)
