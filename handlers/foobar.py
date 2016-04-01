import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps

# This is a temporary route that will be removed when sam is rady
# it is meant to be a tool for modifying and operating on data
class Foobar(tornado.web.RequestHandler):
    cursor = None

    def get(self):
        if Foobar.cursor is None:
            conn = self.application.settings['conn']
            Foobar.cursor = r.db('cufcq_debug').table('Instructor').filter({'instructor_first':''}).run(conn)
        try:
            data = Foobar.cursor.next()
            return self.render('foobar.html', data=data)
        except r.ReqlCursorEmpty:
            self.write("all done!")


    def post(self):
        self.process_post()
        self.get()

    def process_post(self):
        conn = self.application.settings['conn']
        old_instructor_id = self.get_argument('id')
        instructor_data = self.application.settings['instructor'].get_item(old_instructor_id)
        new_instructor_first = self.get_argument('instructor_first')
        new_instructor_last = self.get_argument('instructor_last')
        new_instructor_id = "{0}-{1}".format(new_instructor_last, new_instructor_first)
        new_instructor_id = new_instructor_id.lower()
        instructor_data['instructor_first'] = new_instructor_first
        instructor_data['instructor_last'] = new_instructor_last
        instructor_data['id'] = new_instructor_id
        r.db('cufcq_debug').table('Fcq').filter({'instructor_id': old_instructor_id}).update(
            {
                'instructor_id': new_instructor_id,
                'instructor_first': new_instructor_first,
                'instructor_last': new_instructor_last
            }
        ).run(conn)
        logging.info(instructor_data)
        self.application.settings['instructor'].create_item(instructor_data)
        self.application.settings['instructor'].delete_item(old_instructor_id)
        return
