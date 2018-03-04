# LogsAnalysis
	This application queries a large news database to answer the following 3 questions:
		1) What are the top 3 articles?
		2) Who are the top 3 authors?
		3) On what day(s) were there more than 1% of clicks resulting in service errors?

## Dependencies 
	[VirtualBox](https://www.virtualbox.org/wiki/Downloads) platform package for your operating system.
	[Vagrant](https://www.vagrantup.com/downloads.html)
	[Vagrant Configuration File](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile)

	A SSH client such as the one that comes with the [Github Desktop App](https://desktop.github.com/)
	[newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) 
	
## Setup
	Download all the dependencies.
	
	Install the SSH client. (if you use the one from Github, it is installed when you install the desktop app.)
	
	Install Virtual Box, then install Vagrant.
	
	Create a folder for this application and move the vagrant configuration file into it.
	Inside the folder create a folder and name it newsdata. 
	Move newsdata.sql and this project into the newsdata folder. 
	
	Open a terminal and enter in the following command.
	`vagrant up && vagrant ssh`
	NOTE: At this point you may want to grab a cup of coffee 
	as it will take a few minuets to start up for the first time.
	
	If all goes well you should be logged in to the os as Vagrant and 
	be presented with a prompt. Type in: 
	`cd /vagrant/newsdata`
	psql -d news -f newsdata.sql`
	
	NOTE: Time for an other cup of coffee. This database is large and will take a little while to load.

	The application uses three views that need to be added to the database.
	
	
	You can add them automatically by using **Setup.py** 
	`python3 Setup.py`
	
	**or** you can type them in manually as follows:
	`
	psql -d news
	
	CREATE VIEW clicks AS 
	SELECT title, count(*) AS clicks, author 
	FROM log JOIN articles ON log.path = concat('/article/', articles.slug) 
	GROUP by title, author 
	ORDER by clicks DESC;

	CREATE VIEW Error AS
    	SELECT DATE(time) AS Date, COUNT(status) AS Errors
    	FROM log
    	WHERE status != '200 OK'
    	GROUP BY DATE(time)
    	ORDER BY DATE(time);

    	CREATE VIEW Percent AS
    	SELECT
        error.date,
        CAST(error.errors AS FLOAT) /
            CAST(COUNT(log.status) AS FLOAT) AS Percent
    	FROM error JOIN log ON error.date = DATE(log.time)
    	GROUP BY error.date, error.errors
    	ORDER BY error.date;
	`
## Run
	Please use **Python3** to compile.
	The database uses PostgreSQL
			
	Test.py is included for your convenience. Test.py will create an instance of LogsAnalysis
	and run methods to answer each of the 3 questions.
	
	To run open a terminal and type in "python3 Test.py" 
	note if you forgot to add the required views you can type "python3 Setup.py && python3 Test.py"

## Included Files
	Setup.py
		Automatically sets up the required views.
	LogsAnalysis.py
		Contains the class definition of LogsAnalysis and it's methods.
			Popular_Articles()
			Popular_Authors()
			Bad_Day()
	LogsAnalysis.txt
		Contains a printout of the queries.
	Test.py
		Implements the LogsAnalysis class and runs methods for each of the 3 questions.

	newsdata.sql
		The database provided by Udacity
