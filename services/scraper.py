import mechanize
import logging
import requests
import os


def scrape(campus, firstyear, firstterm, lastyear, lastterm):
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
    xcel_path = "data/raw/{filename}.xls".format(filename=filename)
    output = open(xcel_path, 'wb')
    output.write(r.content)
    output.close()
    csv_path = "data/csv/{filename}.csv".format(filename=filename)
    os.system("ssconvert -S {path} temp.csv > /dev/null".format(path=xcel_path))
    convert_csv('temp.csv.1', csv_path)
    os.system("rm temp.csv.*")
    logging.info("successfully downloaded and parsed {0}".format(csv_path))


def convert_csv(input_file, output_file):
    with open(input_file, 'rb') as f:
        with open(output_file, 'w') as f1:
            for line in f:
                f1.write(line)
            # f.next() # skip header line
            # first = True
            # for line in f:
            #     if first:
            #         # This is the custom header line that our import task wants.
            #         f1.write('yearterm,subject,crse,sec,onlinefcq,bdcontinedcrse,instructor_last,instructor_first,formsrequested,formsreturned,percentage_passed,courseoverall,courseoverall_sd,instructoroverall,instructoroverall_sd,hoursperwkinclclass,priorinterest,instreffective,availability,challenge,howmuchlearned,instrrespect,course_title,courseoverall_old,courseoverall_sd_old,instroverall_old,instroverall_sd_old,r_fair,r_access,workload,r_divstu,r_diviss,r_presnt,r_explan,r_assign,r_motiv,r_learn,r_complx,campus,college,asdiv,level,fcqdpt,instr_group,i_num\n')
            #         # f1.write('yearterm,subject,crse,sec,onlineFCQ,bd_continuing_education,instructor_last,instructor_first,formsrequested,formsreturned,percentage_passed,course_overall,course_overall_SD,instructoroverall,instructoroverall_SD,total_hours,prior_interest,effectiveness,availability,challenge,amount_learned,respect,course_title,courseOverall_old,courseOverall_SD_old,instrOverall_old,instrOverall_SD_old,r_Fair,r_Access,workload,r_Divstu,r_Diviss,r_Presnt,r_Explan,r_Assign,r_Motiv,r_Learn,r_Complx,campus,college,aSdiv,level,fcqdpt,instr_group,i_Num\n')
            #         first = False
            #     else:
            #         # Replace double quotes with null, relace spaced commas with normal commas, replace the big comma chunk with a bigger one for our header.
            #         line = line.replace('"', '').replace(',,,,,,',',,,,,,,,,,,,,,,',1).replace(', ',',',1).replace(', ',' ')
            #         f1.write(line)
