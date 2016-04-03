from handlers.base_handler import BaseHandler


class DepartmentHandler(BaseHandler):
    
    def color(self):
        return 'violet'

    def overtime_instructor_linechart(self, raw_data):
        def _overtime_builder(overtime_data, key):
            def _transform_overtime_data(yearterm):
                return round(overtime_data[str(yearterm)][key], 1)
            return _transform_overtime_data

        def _overtime_dataset_builder(key):
            color = {
                'course_howmuchlearned_average': (247, 92, 3),
                'course_challenge_average': (217, 3, 104),
                'courseoverall_average': (130, 2, 99),
                'course_priorinterest_average': (4, 167, 119)
            }[key]
            label = {
                'course_howmuchlearned_average': 'Amount Learned',
                'course_challenge_average': 'Challenge',
                'courseoverall_average': 'Overall',
                'course_priorinterest_average': 'Prior Interest'
            }[key]
            return {
                'label': label,
                'fillColor': "rgba({0},{1},{2},0.2)".format(*color),
                'strokeColor': "rgba({0},{1},{2},1)".format(*color),
                'pointColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHighlightStroke': "rgba({0},{1},{2},1)".format(*color),
                'pointStrokeColor': "#fff",
                'pointHighlightFill': "#fff",
                'data': list(map(_overtime_builder(overtime_data, key), yearterms))
            }

        keys = [
            'course_howmuchlearned_average',
            'course_challenge_average',
            'courseoverall_average',
            'course_priorinterest_average'
        ]
        yearterms = raw_data['fcqs_yearterms']
        overtime_data = raw_data['fcqs_overtime']
        labels = list(map(self.convert_date, yearterms))
        datasets = list(map(_overtime_dataset_builder, keys))
        return tornado.escape.json_encode({
            'labels': labels,
            'datasets': datasets,
        })

    def get(self, id):
        department = self.application.settings['department'].get_item(id)
        if department is None:
            self.redirect('/notFound')
            return

        self.render('layouts/department_view.html', raw_data=department)
