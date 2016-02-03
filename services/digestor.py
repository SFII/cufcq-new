import csv
import logging
import os
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


def digest(filename):
    if filename == 'ALL':
        allfiles = [f for f in listdir('data/csv/') if isfile(join('data/csv/', f))]
        for f in allfiles:
            print("python3 main.py --digest={0} ".format(f))
            os.system("python3 main.py --digest={0} ".format(f))
        cleanup()
    data = dataSet('data/csv/' + filename)
    for raw_data in data.raw_data:
        generate_fcq(raw_data)


def cleanup():
    cursor = Course().cursor()
    for doc_data in cursor:
        logging.info(doc_data['slug'])
        instructors = list(set(doc_data['instructors']))
        fcqs = list(set(doc_data['fcqs']))
        Course().update_item(doc_data['id'], {'instructors': instructors, 'fcqs': fcqs})
    cursor.close()
    cursor = Instructor().cursor()
    for doc_data in cursor:
        logging.info(doc_data['slug'])
        courses = list(set(doc_data['courses']))
        fcqs = list(set(doc_data['fcqs']))
        Instructor().update_item(doc_data['id'], {'courses': courses, 'fcqs': fcqs})
    cursor.close()
    cursor = Department().cursor()
    for doc_data in cursor:
        logging.info(doc_data['slug'])
        instructors = list(set(doc_data['instructors']))
        courses = list(set(doc_data['courses']))
        fcqs = list(set(doc_data['fcqs']))
        Department().update_item(doc_data['id'], {'instructors': instructors, 'courses': courses, 'fcqs': fcqs})
    cursor.close()


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
