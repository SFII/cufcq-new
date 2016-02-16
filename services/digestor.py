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

# def over_time(db, conn):
#     for model in ['Instructor', 'Course', 'Department']
#     grouped_model = r.db(db).table(model).for_each(
#         lambda doc: r.db(db).table(model).get(doc['id']).update({'over_time': r.db(db).table('Fcq').get_all(*doc['fcqs']).group('yearterm').ungroup().map(
#
#         )})
#     ).run(conn, array_limit=200000)


def _fcq_yearterm_aggregation(fcqs_group_by_yearterm):

    over_time = {}
    fcqs_per_yearterm = {}
    for fcq_yearterm_group in fcq_yearterm_group:
        fcqs_per_yearterm[fcq_yearterm_group["group"]] = fcq_yearterm_group["reduction"]
    for yearterm, fcqs in fcqs_per_yearterm.items():
        over_time[yearterm] = {
            'GR_fcqs': len(_filter_field(fcqs, 'level', 'GR')),
            'UD_fcqs': len(_filter_field(fcqs, 'level', 'UD')),
            'LD_fcqs': len(_filter_field(fcqs, 'level', 'LD')),
            'total_fcqs': len(fcqs),
            'total_students': len()
        }
    return over_time


def _filter_field(iterable, fieldkey, fieldvalue):
    def _filter(item):
        return item[fieldkey] == fieldvalue
    return filter(_filter, iterable)


def _sum_field(iterable, fieldkey):
    stripped = list(filter(None.__ne__, iterable))
    return sum(map(lambda x: return x.get(fieldkey), stripped))


def _average_field(iterable, fieldkey):
    stripped = list(filter(None.__ne__, iterable))
    numberof = len(stripped)
    return _sum_field(stripped, fieldkey) / numberof


def _count_field(iterable, fieldkey, fieldvalue):
    def _filter(item):
        return item[fieldkey] == fieldvalue
    return len(filter(_filter, iterable))


def has_many(db, conn, model, has_many, has_many_id=None):
    model_id = "{0}_id".format(model).lower()
    has_many_plural = "{0}s".format(has_many).lower()
    if not has_many_id:
        has_many_id = "{0}_id".format(has_many).lower()
    grouped_model = r.db(db).table('Fcq').group(model_id).get_field(has_many_id).ungroup().for_each(
        lambda doc: r.db(db).table(model).get(doc["group"]).update({has_many_plural: doc["reduction"].distinct()})
    ).run(conn, array_limit=200000)
    logging.info(grouped_model)

def cleanup(db, conn):
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
