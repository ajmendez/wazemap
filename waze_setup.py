#!/#!/usr/bin/env python
# waze snapshot
# 05.2016

import os
import json
import sqlite3
DB_FILENAME = os.path.expanduser('~/data/waze/data.db')

SETUP = '''
CREATE TABLE IF NOT EXISTS users( 
    id INTEGER PRIMARY KEY ASC, 
    username TEXT, 
    userid TEXT, 
    date INTEGER,
    lon REAL, 
    lat REAL, 
    speed REAL, 
    magvar INTEGER, 
    mood INTEGER
);

CREATE TABLE IF NOT EXISTS alerts( 
    id INTEGER PRIMARY KEY ASC,
    date INTEGER,
    uuid TEXT, 
    type TEXT, 
    subtype TEXT, 
    lon REAL, 
    lat REAL, 
    speed REAL, 
    confidence INTEGER, 
    nComments INTEGER, 
    nthumbsup INTEGER, 
    reliability INTEGER, 
    magvar INTEGER, 
    street TEXT, 
    reportby TEXT
);

CREATE TABLE IF NOT EXISTS jams_line(
    id INTEGER PRIMARY KEY ASC, 
    uuid INTEGER,
    lon REAL,
    lat REAL
);

CREATE TABLE IF NOT EXISTS jams( 
    id INTEGER PRIMARY KEY ASC, 
    uuid TEXT, 
    date INTEGER,
    jam_line_id INTEGER,
    city TEXT,
    delay INTEGER,
    speed REAL,
    severity INTEGER,
    length INTEGER,
    level INTEGER,
    type TEXT,
    turntype TEXT,
    street TEXT,
    updatetime INTEGER,
    pubtime INTEGER
);
'''

def setup(filename):
    if os.path.exists(filename):
        # raise IOError('database already exists: {}'.format(filename))
        pass
    else:
        basedir = os.path.dirname(filename)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.executescript(SETUP)
    
    
    print('Setup done!')
    

if __name__ == '__main__':
    setup(DB_FILENAME)