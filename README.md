# cufcq
http://cufcq.com

## Okay Sam, what is this?
Sam got really excited and remade http://cufcq.com in Python Tornado, with rethinkdb.

## Swiggity. What do I do?
Follow these instructions:

0. Install python dependencies (see `requirements.txt`)
1. `rethinkdb` in the folder, in a seperate terminal tab
2. `Python main.py` to run the site. If you have all dependencies installed, it should begin build the database
3. It should host! But it will be boring cuz theres no data in it. 
4. `Python scraper.py` will scrape the office of planning and budget for data. This command cannot be called in `python3`. In 10 minutes you should have cloned the unorganized Office of planning and budget website. More specific options can be set to download one specific campus or yearterm.
5. `Python3 main.py --digest=20081-BD.csv` will digest that csv file. It takes about 1-2 seconds per file. Run `Python3 main.py --digest=ALL` to digest every csv file. This will take 5 minutes.
6. `Python3 main.py --cleanup` will associate data dependencies, and then build overtime and statistics for each document, tying relevant data together. This will take about 25 minutes.

### Quick Install:
Run `rethinkdb` in a seperate terminal tab. Then:
```
python scraper.py
python3 main.py --digest=ALL
python3 main.py --cleanup
```

After running all of this, you will have an identical and improved database comparable to the current setup. It can also have Colorado Springs and Denver data. All in under an hour.

## What are your plans for this? Why?
If this scq thing is gonna be successful, it needs some strong data already in it. Having the existing fcq data in proximity, and with a simmilar stack as to what we're building, this will give us a chance to superpower scq when it launches. This will also give us a chance to "Bake Two Cakes", if you will. :cake: Because cufcq and scq are simmilar stacks, whatever we find works well in one stack might also work well in the other. It also means we have two opportunities to law down a consistent set of css and javascript, and a consistent set of well-designed handlers and apis. Eventually, we can tie integrations between cufcq and scq, and the result will have a sexy and important "ratemyprofessors" feel to it. We'll need that. As developers, we shouldn't be afraid to tackle code :muscle:

## Isn't this feature creep?
Totes mcgotes it's feature creep. Which is why **I'm taking full responsibility for 100% of cufcq's work.** I've done this once before, and I'll do it again. I have this feature under control, and I can work on it speedily with my resources and experience.

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
* Handlers
* APIs

#### Part 2: Data Integrations
* Search
* Surveys
* Integrate

#### Part 3: Data Party Mansion
* Views
* Charts
* Styling

## Seriously what the hell Sam how did you do this?
![alt tag](http://i.imgur.com/YdmGHYG.gif)
