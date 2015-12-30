#!/usr/bin/python
# -*- coding: utf-8

import MySQLdb
import config

db = MySQLdb.connect(host=config.mysqlhost, user=config.mysqluser, passwd=config.mysqlpass, db=config.mysqldb,
                     charset='utf8')
cursor = db.cursor()
sql = '''
CREATE TABLE `competition` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
try:
    cursor.execute(sql)
    print 'competition table created'
except MySQLdb.Error:
    print(db.error())

sql = '''CREATE TABLE `match` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `competitionId` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `homeTeamId` int(11) DEFAULT NULL,
  `awayTeamId` int(11) DEFAULT NULL,
  `fthg` int(11) DEFAULT NULL,
  `ftag` int(11) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `hthg` int(11) DEFAULT NULL,
  `htag` int(11) DEFAULT NULL,
  `htresult` varchar(255) DEFAULT NULL,
  `hshots` int(11) DEFAULT NULL,
  `ashots` int(11) DEFAULT NULL,
  `htshots` int(11) DEFAULT NULL,
  `atshots` int(11) DEFAULT NULL,
  `hcorners` int(11) DEFAULT NULL,
  `acorners` int(11) DEFAULT NULL,
  `hyellow` int(11) DEFAULT NULL,
  `ayellow` int(11) DEFAULT NULL,
  `hred` int(11) DEFAULT NULL,
  `ared` int(11) DEFAULT NULL,
  `hoffsides` int(11) DEFAULT NULL,
  `aoffsides` int(11) DEFAULT NULL,
  `referee` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `homeTeamId` (`homeTeamId`),
  KEY `awayTeamId` (`awayTeamId`),
  KEY `competitionId` (`competitionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

try:
    cursor.execute(sql)
    print 'match table created'
except MySQLdb.Error:
    print(db.error())

sql = '''CREATE TABLE `team` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `competitionId` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competitionId` (`competitionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

try:
    cursor.execute(sql)
    print 'team table created'
except MySQLdb.Error:
    print(db.error())

sql = '''INSERT INTO `competition` (`title`, `country`, `code`) VALUES
('Premier League', 'England', 'E0')
'''

try:
    cursor.execute(sql)
    print 'init data inserted'
except MySQLdb.Error:
    print(db.error())

db.commit()
db.close()