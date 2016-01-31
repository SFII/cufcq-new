import tornado.ioloop
import tornado.web
import tornado.escape
import unittest
import time
import signal
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import rethinkdb as r
from models.fcq import Fcq
from models.course import Course
from models.instructor import Instructor
from models.department import Department
from config.routes import routes
import logging

define("debug", default=True, help="set True for debug mode", type=bool)
define("test", default=False, help="set True to run Tests", type=bool)
define("scraper", default=False, help="set True to initiate a scraper execution", type=bool)
define('port', default=7000, help='run on the given port', type=int)
define('initalize', default=False, help='run initialize ', type=bool)
define('database_name', default='cufcq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)

settings = {
    'cookie_secret': "8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=",
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'static/',
    'login_url': '/login',
    'fcq': Fcq(),
    'course': Course(),
    'instructor': Instructor(),
    'department': Department(),
}


def initialize():
    settings['debug'] = options.debug
    database_name = options.database_name
    database_port = options.database_port
    database_host = options.database_host
    if options.debug:
        database_name += '-debug'
    if options.test:
        database_name += '-test'
    pass


def main():
    tornado.options.parse_command_line()
    initialize()
    application = tornado.web.Application(handlers=routes, **settings)
    httpserver = HTTPServer(application, xheaders=True)
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0

    # signal handler
    def sig_handler(sig, frame):
        logging.warn("Caught Signal: %s" % sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal handler's callback
    def shutdown():
        logging.info("Stopping HttpServer ...")
        httpserver.stop()  # No longer accept new http traffic
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
        # recursion for terminate IOLoop.instance()

        def terminate():
            now = time.time()
            if now < deadline and (instance._callbacks or instance._timeouts):
                instance.add_timeout(now + 1, terminate)
            else:
                instance.stop()  # After process all _callbacks and _timeouts, break IOLoop.instance()
                logging.info('Shutdown ...')
        # process recursion
        terminate()
    if options.test:
        testsuite = unittest.TestLoader().discover('test')
        return unittest.TextTestRunner(verbosity=2).run(testsuite)
    if options.debug:
        httpserver.listen(options.port if options.port else settings.SITE_PORT)
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
    else:
        httpserver.bind(options.port if options.port else settings.SITE_PORT)  # port
        httpserver.start(0)
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit ...')

if __name__ == "__main__":
    main()
