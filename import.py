#!/usr/bin/python
# -*- coding: utf-8

import MySQLdb
import csv
import urllib2
import config

db = MySQLdb.connect(host=config.mysqlhost, user=config.mysqluser, passwd=config.mysqlpass, db=config.mysqldb,
                     charset='utf8')
db.autocommit(on=True)
cursor = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute('TRUNCATE TABLE `team`')
cursor.execute('TRUNCATE TABLE `match`')


def get_or_create_team(title, comp_id):
    cursor.execute('SELECT `id` FROM `team` WHERE `competitionId` = %s AND `title` = "%s"' % (comp_id, title))
    result = cursor.fetchone()
    if result is None:
        cursor.execute('INSERT INTO `team` (`competitionId`, `title`) VALUES (%s, "%s")' % (comp_id, title))
        cursor.execute('SELECT `id` FROM `team` WHERE `competitionId` = %s AND `title` = "%s"' % (comp_id, title))
        result = cursor.fetchone()

    return result['id']

competition_list = []
season_list = []

for year in range(0, 15, 1):
    season_list.append('%02d%02d' % (year, (year + 1)))

cursor.execute('SELECT * FROM `competition`')
for row in cursor:
    competition_list.append({'id': row['id'], 'code': row['code']})

for season in season_list:
    for competition in competition_list:
        print('process competition %s in season %s' % (competition['code'], season))
        url = config.url_prefix + season + '/' + competition['code'] + '.csv'
        print('download csv: %s' % url)
        response = urllib2.urlopen(url)
        cr = csv.reader(response)

        matches_count = 0
        for row in cr:
            if row[0] != competition['code']:
                continue
            home_team_id = get_or_create_team(row[2], competition['id'])
            away_team_id = get_or_create_team(row[3], competition['id'])
            date_array = row[1].split('/')
            date = '20' + date_array[2] + '-' + date_array[1] + '-' + date_array[0]
            sql = '''INSERT INTO `match` (`competitionId`, `date`, `homeTeamId`, `awayTeamId`, `fthg`, `ftag`,
                  `result`, `hthg`, `htag`, `htresult`, `hshots`, `ashots`, `htshots`, `atshots`, `hcorners`,
                  `acorners`, `hyellow`, `ayellow`, `hred`, `ared`, `hoffsides`, `aoffsides`, `referee`) VALUES (%s,
                  "%s", %s, %s, %s, %s, "%s", %s, %s, "%s", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "%s")''' \
                  % (competition['id'], date, home_team_id, away_team_id, row[4], row[5], row[6], row[7], row[8],
                     row[9], row[12], row[13], row[14], row[15], row[18], row[19], row[22], row[23], row[24],
                     row[25], row[20], row[21], row[11])
            cursor.execute(sql)
            matches_count += 1

        print('season processed. %d matches' % matches_count)