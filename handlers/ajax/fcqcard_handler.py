import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler
import logging


class FcqCardHandler(BaseHandler):
    def get(self, item_id):
        fcq_data = self.application.settings['fcq'].get_item(item_id)
        grade_data = self.application.settings['grade'].get_item(item_id)
        fcq_id = item_id
        date = self.convert_date(fcq_data['yearterm'])
        campus = self.convert_campus(fcq_data['campus'])
        return self.render('modules/fcqdata.html',
                           fcq_id=fcq_id,
                           fcq_data=fcq_data,
                           grade_data=grade_data,
                           date=date,
                           campus=campus)
