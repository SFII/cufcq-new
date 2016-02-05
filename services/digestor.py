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
        print(headers)
        print(len(headers))
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
            print("python3 main.py --digest={0} ".format(f))
            os.system("python3 main.py --digest={0} ".format(f))
        return cleanup(db, conn)
    data = dataSet('data/csv/' + filename)
    fcq_data = list(map(Fcq().sanitize_from_raw, data.raw_data))
    for model in [Department(), Course(), Instructor()]:
        sanitized_data = list(map(model.sanitize_from_raw, fcq_data))
        sanitized_data = list({v['id']: v for v in sanitized_data}.values())
        result = r.db(db).table(model.__class__.__name__).insert(sanitized_data).run(conn)
        logging.info(result)
    result = r.db(db).table('Fcq').insert(fcq_data).run(conn)
    logging.info(result)

def has_many(db, conn, model, has_many, has_many_id=None):
    model_id = "{0}_id".format(model).lower()
    has_many_plural = "{0}s".format(has_many).lower()
    if not has_many_id:
        has_many_id = "{0}_id".format(has_many).lower()
    grouped_model = r.db(db).table('Fcq').group(model_id).get_field(has_many_id).ungroup().distinct().for_each(
        lambda doc: r.db(db).table(model).get(doc["group"]).update({has_many_plural: doc["reduction"]})
    ).run(conn, array_limit=200000)
    logging.info(grouped_model)

def cleanup(db, conn):
    has_many(db, conn, 'Course', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Course', 'Instructor')
    has_many(db, conn, 'Instructor', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Instructor', 'Course')
    has_many(db, conn, 'Department', 'Fcq', has_many_id='id')
    has_many(db, conn, 'Department', 'Instructor')
    has_many(db, conn, 'Department', 'Course')


def generate_fcq_associated_models(fcq_data):
    instructor_id = None
    course_id = None
    department_id = None
    fcq_id = fcq_data['id']
    department_id = fcq_data['department_id']
    instructor_id = fcq_data['instructor_id']
    course_id = fcq_data['course_id']
    if department_id and instructor_id and course_id:
        return fcq_id
    if fcq_data['department_id'] is None:
        department_id = generate_department(fcq_data)

    if fcq_data['instructor_id'] is None:
        instructor_id = generate_instructor(fcq_data, department_id)

    if fcq_data['course_id'] is None:
        course_id = generate_course(fcq_data, department_id)
    logging.info(fcq_id)
    logging.info(course_id)
    logging.info(instructor_id)
    logging.info(department_id)
    Course().append_item_to_listfield(course_id, 'instructors', instructor_id)
    Course().append_item_to_listfield(course_id, 'fcqs', fcq_id)
    Instructor().append_item_to_listfield(instructor_id, 'courses', course_id)
    Instructor().append_item_to_listfield(instructor_id, 'fcqs', fcq_id)
    Department().append_item_to_listfield(department_id, 'instructors', instructor_id)
    Department().append_item_to_listfield(department_id, 'courses', course_id)
    Department().append_item_to_listfield(department_id, 'fcqs', fcq_id)
    updated_ids = {
        'department_id': department_id,
        'course_id': course_id,
        'instructor_id': instructor_id
    }
    Fcq().update_item(fcq_id, updated_ids)
    return fcq_id


def generate_instructor(fcq_data, department_id=None):
    sanitized = Instructor().sanitize_from_raw(fcq_data)
    sanitized['department_id'] = department_id
    slug = sanitized['slug']
    instructor_id = Instructor().create_item(sanitized, quiet=True)
    if instructor_id is None:
        instructor_results = Instructor().find_item({'slug': slug})
        if len(instructor_results):
            instructor_id = instructor_results[0]['id']
        else:
            return logging.error(Instructor().verify(sanitized))
    return instructor_id


def generate_course(fcq_data, department_id=None):
    sanitized = Course().sanitize_from_raw(fcq_data)
    sanitized['department_id'] = department_id
    slug = sanitized['slug']
    course_id = Course().create_item(sanitized, )
    if course_id is None:
        course_results = Course().find_item({'slug': slug})
        if len(course_results):
            course_id = course_results[0]['id']
        else:
            return logging.error(Course().verify(sanitized))
    return course_id


def generate_department(fcq_data):
    sanitized = Department().sanitize_from_raw(fcq_data)
    slug = sanitized['slug']
    department_id = Department().create_item(sanitized)
    if department_id is None:
        department_id = Department().find_item({'slug': slug})[0]['id']
    return department_id


def generate_fcq(raw_data):
    sanitized = Fcq().sanitize_from_raw(raw_data)
    slug = sanitized['slug']
    fcq_id = Fcq().create_item(sanitized)
    if fcq_id is None:
        fcq_results = Fcq().find_item({'slug': slug})
        if len(fcq_results):
            return generate_fcq_associated_models(fcq_results[0])
        else:
            return logging.error(Fcq().verify(sanitized))
    sanitized['id'] = fcq_id
    generate_fcq_associated_models(sanitized)
