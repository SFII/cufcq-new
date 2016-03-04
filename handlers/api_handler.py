import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler
import logging


class ApiHandler(BaseHandler):
    def get(self, table, input):
        model = self.application.settings[table]
        try:
            data = model.get_item(input)
        except:
            self.set_status(401, "no {0} found with id {1}".format(table, input))
            data = None
        logging.info(data)
        return self.write(data)
