#!/usr/bin/env python
__author__ = 'svalleru'
import json
import sys
import os.path
import MySQLdb

survey = {}
RESP_FILE = 'response.json'

# create table using schema @ surveypromptclidb.sql
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = ''
DB_NAME = 'surveypromptclidb'

def db_persist(survey):
    try:
        db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
        cur = db.cursor()
        #delete old records if exists
        cur.execute('''DELETE FROM responses WHERE username = %s''', survey['name'])
        db.commit()
        for k, v in survey.iteritems():
            if k == 'name':
                pass
            else:
                cur.execute('''INSERT INTO responses (username, question, answer)
                      values (%s, %s, %s)''',
                      (survey['name'], k, v))
                db.commit()
        db.close()
        return 'survey stored succesfully..'
    except:
        return 'unable to store! check database settings..'

# takes list of choices, presents to user & returns selected choice
def render_choice(c):
    ctr = 1
    d = {}
    s = ''
    for i in c:
        d[str(ctr)] = i['choice']
        s += '{0}){1}\n'.format(str(ctr), i['choice'])
        ctr += 1
    s += '>>'
    r = raw_input(s)
    # validate input
    try:
        if r == '' or type(int(r)) is not int or int(r) not in range(0, len(d.keys()) + 1):
            print 'invalid choice..exiting..'
            sys.exit(1)
    except:
        print 'invalid choice..exiting..'
        sys.exit(1)

    return d[r]

# recursive question renderer
def render_question(question):
    if 'choices' not in question:  # for questions without any choices
        survey[question['question']] = raw_input('{0}:\n>>'.format(question['question']))
    else:
        print question['question']
        survey[question['question']] = render_choice(question['choices'])
        for f in question['choices']:
            if 'follow-ups' in f.keys() and f['choice'] == survey[question['question']]:
                 for nf in f['follow-ups']:
                     render_question(nf)

def main():
    # read survey template json file name
    if len(sys.argv) <= 1:
        print 'Please provide file name..'
        sys.exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print 'File not found..'
        sys.exit(1)

    with open(sys.argv[1]) as template:
        jlist = json.load(template)
    # read and store user name
    survey['name'] = raw_input('{0}:\n>>'.format('Please enter your full name (first and last)'))
    # ask questions
    for question in jlist:
        render_question(question)

    # uncomment these line to store response into json file
    # #use standard ast.literal_eval to unmarshall response.json
    # with open('response.json', 'ab') as resp:
    #     json.dump(survey, resp)
    #     resp.write('\n')
    print db_persist(survey)

if __name__ == "__main__":
    main()




