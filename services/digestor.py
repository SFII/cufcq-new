import csv
import logging
import os
import rethinkdb as r
from models.fcq import Fcq
from models.instructor import Instructor
from models.course import Course
from models.department import Department
from os import listdir
from os.path import isfile, join


class dataSet:
    """
    Class to store a digested csv
    """
    def __init__(self, location):
        with open(location, "r") as myfile:
            self.headers = self.toArray(myfile.readline())
            self.stringData = myfile.readlines()
            self.raw_data = self.transformData(self.stringData, self.headers)

    def toArray(self, string):
        reader = csv.reader([string], delimiter=',')
        array = []
        for read in reader:
            for a in read:
                array.append(a.strip())
        return array

    def transformData(self, data, headers):
        """
        Input Parameters:
            data: The data that is read from the file. list of strings
            attribute: The attribute you want to consider from the file

        Returns a list of floats parsed from the ithAttribute of the list of strings
        """
        dataArray = []
        for i, string in enumerate(data):
            dataDict = {}
            for j, dataValue in enumerate(self.toArray(string)):
                # print("{0}\t\t{1}".format(headers[j], dataValue))
                dataDict[headers[j]] = dataValue
            dataArray.append(dataDict)
        return dataArray

    def write(self, location, data):
        with open(location, "w") as outfile:
            outfile.write(str(data)[1:-1])


def digest(filename, db, conn):
    if filename == 'ALL':
        allfiles = [f for f in listdir('data/csv/') if isfile(join('data/csv/', f))]
        for f in allfiles:
            logging.info("{0} ".format(f))
            digest_file(f, db, conn)
        return
    else:
        digest_file(filename, db, conn)


def digest_file(filename, db, conn):
    data = dataSet('data/csv/' + filename)
    fcq_data = list(map(Fcq().sanitize_from_raw, data.raw_data))
    for model in [Department(), Course(), Instructor()]:
        sanitized_data = list(map(model.sanitize_from_raw, fcq_data))
        sanitized_data = list({v['id']: v for v in sanitized_data}.values())
        result = r.db(db).table(model.__class__.__name__).insert(sanitized_data).run(conn)
        logging.info(result)
    result = r.db(db).table('Fcq').insert(fcq_data).run(conn)
    logging.info(result)


def cleanup(db, conn):
    associate(db, conn)
    overtime(db, conn)
    # stats_data(db, conn)
    # grade_data(db, conn)


def build_overtime(model):
    def _general_overtime():
        return {
            'GR_fcqs': 0,  # len(_filter_field(fcqs, 'level', 'GR')),
            'UD_fcqs': 0,  # len(_filter_field(fcqs, 'level', 'UD')),
            'LD_fcqs': 0,  # len(_filter_field(fcqs, 'level', 'LD')),
            'total_fcqs': 0,  # len(fcqs),
            'total_forms_requested': 0,  # _sum_field(fcqs, 'forms_requested'),
            'total_forms_returned': 0  # _sum_field(fcqs, 'forms_returned')
        }

    def _instructor_overtime(unchained=False):
        ot = {
            'total_courses': 0,  # len(_distinct_field(fcqs, 'course_id')),
            'instructoroverall_average': 0  # _average_field(fcqs, 'instructoroverall'),
        }
        chain = {} if unchained else _general_overtime()
        ot.update(chain)
        return ot

    def _course_overtime(unchained=False):
        ot = {
            'total_instructors': 0,  # len(_distinct_field(fcqs, 'instructor_id')),
            'courseoverall_average': 0  # _average_field(fcqs, 'courseoverall'),
        }
        chain = {} if unchained else _general_overtime()
        ot.update(chain)
        return ot

    def _depertment_overtime():
        cot = _course_overtime(unchained=True)
        iot = _instructor_overtime(unchained=True)
        got = _general_overtime()
        dot = {
            'TA_instructors': 0,  # len(_filter_field(_distinct_field(fcqs, 'instructor_id'), 'level', 'TA')),
            'OTH_instructors': 0,  # len(_filter_field(_distinct_field(fcqs, 'instructor_id'), 'level', 'OTH')),
            'TTT_instructors': 0,  # len(_filter_field(_distinct_field(fcqs, 'instructor_id'), 'level', 'TTT')),
            'GR_courses': 0,  # len(_filter_field(_distinct_field(fcqs, 'course_id'), 'level', 'GR')),
            'UD_courses': 0,  # len(_filter_field(_distinct_field(fcqs, 'course_id'), 'level', 'UD')),
            'LD_courses': 0,  # len(_filter_field(_distinct_field(fcqs, 'course_id'), 'level', 'LD')),
            'TA_instructoroverall_average': 0,  # _average_field(_filter_field(fcqs, 'instructor_group', 'TA'), 'instructoroverall'),
            'OTH_instructoroverall_average': 0,  # _average_field(_filter_field(fcqs, 'instructor_group', 'OTH'), 'instructoroverall'),
            'TTT_instructoroverall_average': 0,  # _average_field(_filter_field(fcqs, 'instructor_group', 'TTT'), 'instructoroverall'),
            'GR_courseoverall_average': 0,  # _average_field(_filter_field(fcqs, 'level', 'GR'), 'courseoverall'),
            'UD_courseoverall_average': 0,  # _average_field(_filter_field(fcqs, 'level', 'UD'), 'courseoverall'),
            'LD_courseoverall_average': 0  # _average_field(_filter_field(fcqs, 'level', 'LD'), 'courseoverall'),
        }
        dot.update(cot)
        dot.update(iot)
        dot.update(got)
        return dot
    return {
        'Instructor': _instructor_overtime(),
        'Course': _course_overtime(),
        'Department': _depertment_overtime()
    }[model]


def has_many(db, conn, model, has_many, has_many_id=None):
    model_id = "{0}_id".format(model).lower()
    has_many_plural = "{0}s".format(has_many).lower()
    if not has_many_id:
        has_many_id = "{0}_id".format(has_many).lower()
    grouped_model = r.db(db).table('Fcq').group(model_id).get_field(has_many_id).ungroup().for_each(
        lambda doc: r.db(db).table(model).get(doc["group"]).update({has_many_plural: doc["reduction"].distinct()})
    ).run(conn, array_limit=200000)
    logging.info(grouped_model)


def overtime(db, conn):
    department_overtime = r.db(db).table('Department').merge(lambda doc:
        {'fcq_data': r.db('cufcq_debug').table('Fcq').get_all(r.args(doc['fcqs'])).coerce_to('array')}
    ).for_each(
        lambda doc: r.db(db).table('Department').get(doc['id']).update({'overtime': doc['fcq_data'].group('yearterm').ungroup().map(
            lambda val: [val["group"].coerce_to('string'), {
                'GR_fcqs': val["reduction"].filter({'level': 'GR'}).count(),
                'UD_fcqs': val["reduction"].filter({'level': 'UD'}).count(),
                'LD_fcqs': val["reduction"].filter({'level': 'LD'}).count(),
                'total_fcqs': val["reduction"].count(),
                'total_forms_requested': val["reduction"].sum('forms_requested'),
                'total_forms_returned': val["reduction"].sum('forms_returned'),
                'GR_courses': val["reduction"].filter({'level': 'GR'}).get_field('course_id').distinct().count(),
                'UD_courses': val["reduction"].filter({'level': 'UD'}).get_field('course_id').distinct().count(),
                'LD_courses': val["reduction"].filter({'level': 'LD'}).get_field('course_id').distinct().count(),
                'total_courses': val["reduction"].get_field('course_id').distinct().count(),
                'TA_instructors': val["reduction"].filter({'instructor_group': 'TA'}).get_field('instructor_id').distinct().count(),
                'OTH_instructors': val["reduction"].filter({'instructor_group': 'OTH'}).get_field('instructor_id').distinct().count(),
                'TTT_instructors': val["reduction"].filter({'instructor_group': 'TTT'}).get_field('instructor_id').distinct().count(),
                'total_instructors': val["reduction"].get_field('instructor_id').distinct().count(),
                'instructoroverall_average': val["reduction"].get_field('instructoroverall').avg().default(None),
                'TA_instructoroverall_average': val["reduction"].filter({'instructor_group': 'TA'}).get_field('instructoroverall').avg().default(None),
                'OTH_instructoroverall_average': val["reduction"].filter({'instructor_group': 'OTH'}).get_field('instructoroverall').avg().default(None),
                'TTT_instructoroverall_average': val["reduction"].filter({'instructor_group': 'TTT'}).get_field('instructoroverall').avg().default(None),
                'courseoverall_average': val["reduction"].get_field('courseoverall').avg().default(None),
                'GR_courseoverall_average': val["reduction"].filter({'level': 'GR'}).get_field('courseoverall').avg().default(None),
                'UD_courseoverall_average': val["reduction"].filter({'level': 'UD'}).get_field('courseoverall').avg().default(None),
                'LD_courseoverall_average': val["reduction"].filter({'level': 'LD'}).get_field('courseoverall').avg().default(None),
            }]
        ).coerce_to('object')})
    ).run(conn, array_limit=200000)
    logging.info(department_overtime)


def associate(db, conn):
    has_many(db, conn, 'Course', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Course', 'yearterm', has_many_id='yearterm')
    has_many(db, conn, 'Course', 'alternate_title', has_many_id='course_title')
    has_many(db, conn, 'Course', 'Instructor')
    has_many(db, conn, 'Instructor', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Instructor', 'yearterm', has_many_id='yearterm')
    has_many(db, conn, 'Instructor', 'Course')
    has_many(db, conn, 'Department', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Department', 'yearterm', has_many_id='yearterm')
    has_many(db, conn, 'Department', 'Instructor')
    has_many(db, conn, 'Department', 'Course')
