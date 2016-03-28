# cufcq
Sam got really excited and remade http://cufcq.com in Python Tornado, with rethinkdb.

## Swiggity. What do I do?
Follow these instructions:

0. Install python dependencies (see `requirements.txt`)
1. `rethinkdb` in a seperate terminal tab
2. `python3 main.py` to run the site. If you have all dependencies installed, it should begin build the database
3. It should host! But it will be boring cuz theres no data in it.

## Quick Data provisioning
`python3 main.py --restore=xxx`, where `xxx` is the name of the `.tar.gz` backup of the database you can load up.

## What else needs to be done?

#### Part 0: Database
* ~~Boilerplate~~
* ~~Scraper~~
* ~~Generator~~

#### Part 1: Data Fort Knox
* ~~Precomputed Data~~
  * ~~Associations~~
  * ~~Stats~~
  * ~~Chronology~~
* ~~Handlers~~
* ~~Ultrafast Data Backup and Restore~~
* APIs
  * ~~jsons of everything~~
  * Other suggestions

#### Part 2: Data Integrations
* ~~Search~~
* Surveys
* Integrate

#### Part 3: Data Party Mansion
* Views
  * Instructors
  * Courses
  * Departments
  * College
  * Campus
  * Static Pages
* Charts
  * ~~Overtime Lines~~
  * ~~Pie Charts~~
  * Grade Stack Charts
  * A wicked sick d3 viz
* Styling
