import logging
import requests
import os
import sys
import argparse
import time
if sys.version_info[0] < 3:
    import mechanize

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--grades', type=bool, nargs=1, default=False, help='if scraping, whether to additionally download the grades .xlsm file')
parser.add_argument('--fterm', type=int, nargs=1, default=1, help='if scraping, the first term to consider. 1 is Spring, 4 is Summer, 7 is Fall.')
parser.add_argument('--lterm', type=int, nargs=1, default=7, help='if scraping, the last term to consider. 1 is Spring, 4 is Summer, 7 is Fall.')
parser.add_argument('--fyear', type=int, nargs=1, default=2008, help='if scraping, the first year to consider. 2008 is the earliest.')
parser.add_argument('--lyear', type=int, nargs=1, default=2015, help='if scraping, the last year to consider.')
parser.add_argument('--campus', type=str, nargs=1, default='BD', choices=['BD', 'DN', 'CS'], help='if scraping, the campus to scrape. BD is boulder, DN is denver, CS is Colorado Springs')


def scrape(campus, firstyear, firstterm, lastyear, lastterm):
    if sys.version_info[0] >= 3:
        return logging.error("scraper must be run with python version <= 2.5")
    if not verify_options(campus, firstyear, firstterm, lastyear, lastterm):
        return logging.error("bad inputs: {0}, {1}, {2}, {3}, {4}".format(campus, firstyear, firstterm, lastyear, lastterm))
    fcqdpt = {
        'BD': 'BD : Entire Campus ## BD',
        'DN': 'DN : Entire Campus ## DN',
        'CS': 'CS : Entire Campus ## CS'
    }[campus]
    url = {
        'BD': 'https://fcq.colorado.edu/UCBdata.htm',
        'DN': 'https://fcq.colorado.edu/UCDdata.htm',
        'CS': 'https://fcq.colorado.edu/uccsdata2.htm'
    }[campus]
    firstyearterm = firstyear * 10 + firstterm
    lastyearterm = lastyear * 10 + lastterm
    for yearterm in range(firstyearterm, lastyearterm + 1):
        year = yearterm / 10
        term = yearterm % 10
        if term not in [1, 4, 7]:
            continue
        filename = download_fcq(str(year), str(term), fcqdpt, url)
        time.sleep(1)
    return


def verify_options(campus, firstyear, firstterm, lastyear, lastterm):
    if campus not in ['BD', 'DN', 'CS']:
        return False
    if firstyear not in range(2008, 2050):
        return False
    if lastyear not in range(2008, 2050):
        return False
    if firstterm not in [1, 4, 7]:
        return False
    if lastterm not in [1, 4, 7]:
        return False
    return True


def download_grades():
    r = requests.get('http://www.colorado.edu/pba/course/gradesall.xlsm')
    filename = "grades"
    xcel_path = "data/raw/{filename}.xls".format(filename=filename)
    output = open(xcel_path, 'wb')
    output.write(r.content)
    output.close()
    csv_path = "data/grades/{filename}.csv".format(filename=filename)
    os.system("ssconvert -S {path} temp.csv > /dev/null".format(path=xcel_path))
    convert_csv('temp.csv.2', csv_path)
    os.system("rm temp.csv.*")
    os.system("tail -n +10 {path} > {path}.tmp && mv {path}.tmp {path}".format(path=csv_path))


def download_fcq(year, term, fcqdpt, url):
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]
    # open the url
    response = br.open(url)
    control = br.select_form("frmFCQ")
    fileFrmt = 'XLS'
    grp1 = 'ALL'
    # go through all of the form options so we can change them
    for control in br.form.controls:
        # this will show us all of our default value for the fields. See page options for the output of the FCQ page as of 1/3/15
        if (control.name == 'fcqdpt'):
            br[control.name] = [fcqdpt]
            logging.info("CHANGE fcqdpt type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
        elif (control.name == 'ftrm'):
            br[control.name] = [term]
            logging.info("CHANGE first term type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
        elif (control.name == 'ltrm'):
            br[control.name] = [term]
            logging.info("CHANGE last term type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
        elif (control.name == 'fileFrmt'):
            br[control.name] = [fileFrmt]
            logging.info("CHANGE fileFrmt type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
        elif (control.name == 'fyr'):
            br[control.name] = [year]
            logging.info("CHANGE first year type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
        elif (control.name == 'lyr'):
            br[control.name] = [year]
            logging.info("CHANGE last year type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
    response = br.submit()
    for link in br.links():
        if (link.text == 'Click here'):
            logging.info(link.url)
            original = link.url
            # need to split because output link is: javascript:popup('/fcqtemp/BD010395426.xls','BD010395426','750','550','yes','yes')
            split = original.replace("\'", '').split(',')
            # get this BD010395426
            proper_link = "https://fcq.colorado.edu/fcqtemp/{xcel}.xls".format(xcel=split[1])
            logging.info(proper_link)
    r = requests.get(proper_link)
    filename = "{year}{term}-{campus}".format(year=year, term=term, campus=fcqdpt[0:2])
    os.system("mkdir -p data/raw/")
    os.system("mkdir -p data/csv/")
    xcel_path = "./data/raw/{filename}.xls".format(filename=filename)
    output = open(xcel_path, 'wb')
    output.write(r.content)
    output.close()
    csv_path = "./data/csv/{filename}.csv".format(filename=filename)
    os.system("ssconvert -S {path} temp.csv > /dev/null".format(path=xcel_path))
    convert_csv('temp.csv.1', csv_path)
    os.system("rm temp.csv.*")
    logging.info("successfully downloaded and parsed {0}".format(csv_path))


def convert_csv(input_file, output_file):
    with open(input_file, 'rb') as f:
        with open(output_file, 'w') as f1:
            for line in f:
                f1.write(line)

if __name__ == "__main__":
    a = parser.parse_args()
    if(a.grades):
        download_grades()
    else:
        scrape(a.campus, a.fyear, a.fterm, a.lyear, a.lterm)
