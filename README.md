# cufcq
http://cufcq.com

## Okay Sam, what is this?
Sam got really excited and remade http://cufcq.com in Python Tornado.

## Holy shit, you did that?
Yeah buddy. You better believe it.

## Swiggity. What do I do?
Follow these instructions:

1. Install python dependencies (see `requirements.txt`)
2. `Python main.py` to run the site. If you have all dependencies installed, it should begin build the database
3. It should host! But it will be boring.
4. `Python main.py --scraper=True` will scrape the office of planning and budget for data. In 10 minutes you should have cloned the unorganized Office of planning and budget website. More specific options can be set to download one specific campus or yearterm.
5. `Python3 main.py --digest=20081-BD.csv` will digest that csv file. It takes about 10-20 minutes per file. Run `Python3 main.py --digest=ALL` to digest every csv file. This will take all night.
6. `Python3 main.py --cleanup=True` will cleanup the DB. This will take about 30 minutes.

After running all of this, you will have an identical and improved database comparable to the current setup. It can also have Colorado Springs and Denver data

## Seriously what the hell Sam how did you do this?
![alt tag](http://i.imgur.com/YdmGHYG.gif)
