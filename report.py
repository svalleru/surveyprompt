#!/usr/bin/env python
__author__ = 'svalleru'
from main import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from prettytable import PrettyTable
import MySQLdb

#print DB_HOST, DB_USER, DB_PASSWD, DB_NAME

try:
    rdb = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
    rcur = rdb.cursor()
    rcur.execute('''SELECT username, question, answer FROM responses''')
    rows = rcur.fetchall()
    users = set()
    rdict = {'q': {'c': 0}}
    for row in rows:
        users.add(row[0])
        if row[1] in rdict.keys():
            if row[2] in rdict[row[1]]:
                rdict[row[1]][row[2]] += 1
            else:
                rdict[row[1]][row[2]] = 1
        else:
                rdict[row[1]] = {}
                rdict[row[1]][row[2]] = 1
    del rdict['q']
    rdb.close()
except Exception as e:
    print 'check database settings!..', e

print '############ SURVEY REPORT ############'
print 'Total number of users who took the survey:', len(users)
# print list(users)
for q, c in rdict.iteritems():
    print 'Q:', q
    r = PrettyTable(c.keys())
    r.add_row(c.values())
    print r
