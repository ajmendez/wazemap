#!/usr/bin/env python
# waze snapshot
# 05.2016

import os
import json
import requests
import sqlite3
from pprint import pprint
from datetime import datetime
from collections import OrderedDict

from waze_setup import DB_FILENAME
con = sqlite3.connect(DB_FILENAME)
cur = con.cursor()



NOW = int(datetime.now().strftime('%s'))*1000
URL = 'https://www.waze.com/rtserver/web/TGeoRSS'
BBOX = []
PARAMS = dict(
    ma = 600,
    mj = 200, # number of jams
    mu = 200, # number of users?
    #bounding box
    left=-122.29225158691405,
    right=-121.83082580566406,
    bottom=37.30197581405354,
    top=37.48658068765521,
    _=NOW, # request date / last request?
)



def get_data():
    '''Scrape the json endpoint for the userinfo'''
    response = requests.get(URL, params=PARAMS)
    # assert response.code == 200, IOError('Failed to get request')
    return response.json()
    
    
def _get(item, name, outname):
    '''
    return the value from item either with a default value, with a function, or as a subdirectory.
    '''
    try:
        # either apply a function or grab with a default value
        if isinstance(name, tuple):
            if hasattr(name[1], '__call__'):
                return name[1](item, name[0], outname)
            else:
                return item.get(name[0], name[1])
        
        # Go down the tree a bit
        elif '.' in name:
            t = name.split('.')
            return item[t[0]][t[1]]
        
        # Simple request
        else:
            return item[name]
    except Exception as e:
        print(name)
        pprint(item)
        raise e


def _len(name):
    cur.execute('SELECT COUNT(*) from {name}'.format(name=name))
    return cur.fetchone()[0]


def _item(data, name, tags):
    '''Gather the right bits for each dataframe'''
    items = data[name]
    out = []
    for item in items:
        tmp = tuple(_get(item, inkey, outkey) for outkey,inkey in tags.items())
        out.append(tmp)
    statement = 'INSERT INTO {name}({tags}) VALUES ({values})'.format(
        name=name,
        tags=','.join(tags.keys()),
        values=','.join(['?' for t in tags.keys()])
    )
    cur.executemany(statement, out)
    print('Finished {name}\n    Added: {added:,d}\n    Total: {total:,d}'.format(
             name=name, added=len(out), total=_len(name),
    ))
    con.commit()


def save_alerts(data):
    tags = OrderedDict(
        date=('xxxdate', NOW),
        uuid='uuid',
        type='type',
        subtype='subtype',
        lon='location.x',
        lat='location.y',
        speed='speed',
        confidence='confidence',
        nComments='nComments',
        nthumbsup='nThumbsUp',
        reliability='reliability',
        magvar='magvar',
        street=('street', ''),
        reportby=('reportBy', ''),
    )
    _item(data, 'alerts', tags)


def save_users(data):
    tags = OrderedDict(
        date=('xxxdate', NOW),
        username='userName',
        userid='id',
        lon='location.x',
        lat='location.y',
        speed='speed',
        magvar='magvar',
        mood='mood',
    )
    _item(data, 'users', tags)





def jams_line(item, name, outname):
    line = item[name]
    uuid = item['uuid']
    items = [(uuid, l['x'], l['y']) for l in line]
    statement = 'INSERT INTO {name}({tags}) VALUES ({values})'.format(
        name = 'jams_line',
        tags = 'uuid,lon,lat',
        values='?,?,?')
    
    cur.executemany(statement, items)
    return uuid
    

def save_jams(data):
    tags = OrderedDict(
        date=('xxxdate', NOW),
        uuid='uuid',
        jam_line_id=('line', jams_line),
        speed='speed',
        city=('city',''),
        delay='delay',
        severity='severity',
        length='length',
        level='level',
        type='type',
        turntype='turnType',
        street=('street', ''),
        updatetime='updateMillis',
        pubtime='pubMillis',
    )
    _item(data, 'jams', tags)
    
def main():
    data = get_data()
    save_alerts(data)
    save_users(data)
    save_jams(data)


if __name__ == '__main__':
    main()
    con.close()

