import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler
import logging


class SearchHandler(BaseHandler):
    def get(self, table, input):
        def _fail():
            self.set_status(401, "no {0} found with id {1}".format(table, input))
            return ""
        model = self.application.settings[table]
        try:
            data = model.get_item(input)
        except:
            data = _fail()
        if data is None:
            data = _fail()
        logging.info(data)
        return self.write(data)
