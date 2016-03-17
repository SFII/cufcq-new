import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler
import logging


class FcqCardHandler(BaseHandler):
    def get(self, item_id):
        fcq_data = self.application.settings['fcq'].get_item(item_id)
        grade_data = self.application.settings['grade'].get_item(item_id)
        return self.render('cards/fcqcard.html',
                           fcq_data=fcq_data,
                           grade_data=grade_data)
