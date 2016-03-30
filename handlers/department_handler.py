import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler

class DepartmentHandler(BaseHandler):
    def get(self):
        department = self.application.settings['department'].get_item(id)
        if department is None:
            # 404 goes here
            return
        return
