#! /usr/bin/env python3

import psycopg2
from datetime import datetime


class LogsAnalysis():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    def __del__(self):
        self.db.close()

    def Popular_Articles(self):
        '''
        Returns an sql query of the top 3 articles sorted by viewing popularity
        with the most popular at the top of the list'''

        self.c.execute('SELECT title, clicks FROM clicks limit 3;')
        data = self.c.fetchall()

        print("\nPopular Articles\n")
        for row in data:
            print('"{}" - {} views'.format(row[0], row[1]))

    def Popular_Authors(self):
        '''Returns an sql query of the top 3 Authors sorted by
            the number of times all their articles have been viewed
        '''
        sql = '''
            SELECT authors.name, SUM(clicks)
            FROM authors JOIN clicks
            ON authors.id = clicks.author
            WHERE authors.name != 'Anonymous Contributor'
            GROUP BY authors.name
            ORDER BY SUM(clicks) DESC
            LIMIT 3;
            '''
        self.c.execute(sql)
        data = self.c.fetchall()
        print("\nPopular Authors\n")
        for row in data:
            print('{} - {} views'.format(row[0], row[1]))

    def Bad_Day(self):
        '''Displays days where more than 1% of requests lead to errors.'''

        QUERY = '''SELECT * FROM Percent WHERE percent > 0.01;'''

        self.c.execute(QUERY)
        data = self.c.fetchall()
        print("\nDays with more than 1% server errors\n")
        for row in data:
            day = '{:%B %d, %Y}'.format(row[0])
            errors = '{:.1%}'.format(row[1])
            print('{} - {} errors'.format(day, errors))
