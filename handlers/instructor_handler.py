import tornado.web
import tornado.template

class InstructorHandler(tornado.web.RequestHandler):
	def get(self):
		instructor_info_object = {
			"first_name" : "John",
			"last_name" : "Black",
			"department" : "Computer Science",
			"type" : "TTT",
			"sections" : 12,
			"courses" : 4,
			"last_fcq" : "Spring 2015",
			"first_fcq" : "Spring 2012",
		}
		instructor_stats_object = {
			"effectiveness" : 5,
			"overall" : 5,
			"availability" : 5,
			"respect" : 5,
		}
		self.render('layouts/instructor_view.html',
			instructor_info=instructor_info_object,
			instructor_stats=instructor_stats_object)
