import signal
import time
import unittest
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from config.application import make_application, initialize_settings
from services.digestor import digest, cleanup, associate, overtime
import logging

define('debug', default=True, help='set True for debug mode', type=bool)
define('test', default=False, help='set True to run Tests', type=bool)
define('port', default=7000, help='run on the given port', type=int)
define('initalize', default=False, help='run initialize ', type=bool)
define('database_name', default='cufcq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)
define('digest', group='digestor', default='',
       help='define explicitly to digest that csv. ALL will digest every .csv', type=str)
define('associate', group='digestor', default=False,
       help='this will build all has-many associations between models', type=bool)
define('overtime', group='digestor', default=False,
       help='this will make all overtime associations', type=bool)
define('cleanup', group='digestor', default=False,
       help='define explicitly to finalize and clean the database', type=bool)


def main():
    """Main entry point for our application"""
    tornado.options.parse_command_line()
    settings = initialize_settings()
    application = make_application(settings)
    httpserver = HTTPServer(application, xheaders=True)
    max_wait_seconds_before_shutdown = 0

    # signal handler
    def sig_handler(sig, frame):
        logging.warn("Caught Signal: {0}".format(sig))
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal handler's callback
    def shutdown():
        logging.info("Stopping HttpServer ...")
        httpserver.stop()  # No longer accept new http traffic
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + max_wait_seconds_before_shutdown
        # recursion for terminate IOLoop.instance()

        def terminate():
            now = time.time()
            if now < deadline:
                instance.add_timeout(now + 1, terminate)
            else:
                instance.stop()
                logging.info('Shutdown ...')

        terminate()
    if options.test:
        testsuite = unittest.TestLoader().discover('test')
        return unittest.TextTestRunner(verbosity=2).run(testsuite)
    if options.digest != '':
        return digest(options.digest, settings['database_name'], settings['conn'])
    if options.associate:
        return associate(settings['database_name'], settings['conn'])
    if options.overtime:
        return overtime(settings['database_name'], settings['conn'])
    if options.cleanup:
        return cleanup(settings['database_name'], settings['conn'])
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
