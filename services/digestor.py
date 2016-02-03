import csv
import logging
import os
from models.fcq import Fcq
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
            self.dictData = self.transformData(self.stringData, self.headers)

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
        return
    data = dataSet('data/csv/' + filename)
    print(data.headers)
    for value in data.dictData:
        sanitized = Fcq().sanitize_from_raw(value)
        fcq_id = Fcq().create_item(sanitized)
        logging.info(fcq_id)
