import tornado.ioloop
import tornado.web
import tornado.escape
from settings.settings import settings
import time
import signal
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import rethinkdb as r
from common.log_utils import getLogger
from models.fcq import Fcq
from models.course import Course
from models.instructor import Instructor
from models.department import Department
from models.campus import Campus
log = getLogger('main.py')

define("port", default=settings.SITE_PORT, help="run on the given port", type=int)
define("debug", default=True, help="set True for debug mode", type=bool)
define("test", default=False, help="set True to run Tests", type=bool)
define("scraper", default=False, help="set True to initiate a scraper execution", type=bool)
define('port', default=7000, help='run on the given port', type=int)
define('initalize', default=False, help='run initialize ', type=bool)
define('database_name', default='cufcq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)

SETTINGS = {
    'cookie_secret': "8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=",
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'static/',
    'login_url': '/login'
    'fcq': Fcq()
    'course': Course()
    'instructor': Instructor()
    'department': Department()
    'campus': Campus()
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
    tornado.locale.load_translations(settings['translations'])
    initalize()
    application = tornado.web.Application(handlers=routes, **SETTINGS)
    httpserver = HTTPServer(application, xheaders=True)
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 10


    # signal handler
    def sig_handler(sig, frame):
        log.warn("Caught Signal: %s" % sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal handler's callback
    def shutdown():
        log.info("Stopping HttpServer ...")
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
                log.info('Shutdown ...')

        # process recursion
        terminate()
    if options.debug:
        httpserver.listen(options.port if options.port else settings.SITE_PORT)
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
    else:
        httpserver.bind(options.port if options.port else settings.SITE_PORT)  # port
        httpserver.start(0)
    tornado.ioloop.IOLoop.instance().start()
    log.info('Exit ...')

if __name__ == "__main__":
    main()
