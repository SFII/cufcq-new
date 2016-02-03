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
from services.scraper import scrape
from services.digestor import digest
from services.generator import generate
import logging

define('debug', default=True, help='set True for debug mode', type=bool)
define('test', default=False, help='set True to run Tests', type=bool)
define('port', default=7000, help='run on the given port', type=int)
define('initalize', default=False, help='run initialize ', type=bool)
define('database_name', default='cufcq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)
define('scraper', group='scraper', default=False, help='set True to initiate an fcq data scraping', type=bool)
define('convert', group='scraper', default=False, help='if scraping, convert the dataset', type=bool)
define('firstterm', group='scraper', default=1, help='if scraping, the first term to consider. 1 is Spring, 4 is Summer, 7 is Fall.', type=int)
define('lastterm', group='scraper', default=7, help='if scraping, the last term to consider. 1 is Spring, 4 is Summer, 7 is Fall.', type=int)
define('firstyear', group='scraper', default=2008, help='if scraping, the first year to consider. 2008 is the earliest.', type=int)
define('lastyear', group='scraper', default=2015, help='if scraping, the last year to consider.', type=int)
define('campus', group='scraper', default='BD', help='if scraping, the campus to scrape. BD is boulder, DN is denver, CS is Colorado Springs', type=str)
define('digest', group='digestor', default='', help='define explicitly to digest that csv. ALL will digest every .csv', type=str)
define('generate', group='generator', default=False, help='set to true to invoke the data generator.', type=bool)

settings = {
    'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'templates/static/',
    'login_url': '/login',
    'fcq': Fcq(),
    'course': Course(),
    'instructor': Instructor(),
    'department': Department(),
}


def initialize():
    settings['debug'] = options.debug
    settings['site_port'] = options.port
    database_name = options.database_name
    database_port = options.database_port
    database_host = options.database_host
    if options.debug:
        database_name += '_debug'
    if options.test:
        database_name += '_test'
    try:
        conn = r.connect(host=options.database_host, port=options.database_port)
        r.db_create(database_name).run(conn)
    except Exception as e:
        logging.warn(e.message)
    settings['fcq'].init(database_name, conn)
    settings['course'].init(database_name, conn)
    settings['instructor'].init(database_name, conn)
    settings['department'].init(database_name, conn)


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
    if options.scraper:
        return scrape(options.campus, options.firstyear, options.firstterm, options.lastyear, options.lastterm)
    if options.digest != '':
        return digest(options.digest)
    if options.generate:
        return generate()
    if options.debug:
        httpserver.listen(settings['site_port'])
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
    else:
        httpserver.bind(settings['site_port'])  # port
        httpserver.start(0)
    logging.info("Now serving on http://localhost:{0}".format(settings['site_port']))
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit ...')


if __name__ == "__main__":
    main()
