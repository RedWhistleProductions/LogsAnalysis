#! /usr/bin/env python3

import psycopg2
db = psycopg2.connect("dbname=news")
c = db.cursor()

'''Creates Views to simplify my SQL queries.'''

CLICKS_VIEW = '''
    CREATE VIEW clicks AS
        SELECT title, COUNT(*) as clicks, author
        FROM log JOIN articles
        ON log.path = CONCAT('/article/', articles.slug)
        GROUP BY title, author
        ORDER BY clicks DESC;
'''

ERROR_VIEW = '''CREATE VIEW Error AS
    SELECT DATE(time) AS Date, COUNT(status) AS Errors
    FROM log
    WHERE status != '200 OK'
    GROUP BY DATE(time)
    ORDER BY DATE(time);'''

PERCENT_VIEW = '''
    CREATE VIEW Percent AS
    SELECT
        error.date,
        CAST(error.errors AS FLOAT) /
            CAST(COUNT(log.status) AS FLOAT) AS Percent
    FROM error JOIN log ON error.date = DATE(log.time)
    GROUP BY error.date, error.errors
    ORDER BY error.date;'''

c.execute(CLICKS_VIEW)
c.execute(ERROR_VIEW)
c.execute(PERCENT_VIEW)
db.commit()
db.close()
