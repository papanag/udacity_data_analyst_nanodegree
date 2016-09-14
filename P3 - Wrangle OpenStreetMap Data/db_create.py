import sqlite3
import os
import csv

# create database
def create_db(filename):
    file_exists = os.path.isfile(filename)
    if file_exists:
        os.remove(filename)
    print ''' "{}" database successfully created '''.format(filename)
    con = sqlite3.connect(filename)
    return con

con = create_db('osm.sqlite')
con.text_factory = str
c = con.cursor()


# create tables
query = 'CREATE TABLE nodes (id INTEGER PRIMARY KEY, lat REAL, lon REAL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT);'
c.execute(query)

query = 'CREATE TABLE nodes_tags (id INTEGER, key TEXT, value TEXT, type TEXT);'
c.execute(query)

query = 'CREATE TABLE ways (id INTEGER PRIMARY KEY, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT);'
c.execute(query)

query = 'CREATE TABLE ways_nodes (id INTEGER, node_id INTEGER, position INTEGER);'
c.execute(query)

query = 'CREATE TABLE ways_tags (id INTEGER, key TEXT, value TEXT, type TEXT);'
c.execute(query)

print 'Created tables successfully'


# import csv into tables
with open('nodes.csv','rb') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        query = 'INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
        params = (row['id'], row['lat'], row['lon'], row['user'], row['uid'], row['version'], row['changeset'], row['timestamp'])
        c.execute(query, params)

with open('nodes_tags.csv','rb') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        query = 'INSERT INTO nodes_tags VALUES (?, ?, ?, ?);'
        params = (row['id'], row['key'], row['value'], row['type'])
        c.execute(query, params)

with open('ways.csv','rb') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        query = 'INSERT INTO ways VALUES (?, ?, ?, ?, ?, ?);'
        params = (row['id'], row['user'], row['uid'], row['version'], row['changeset'], row['timestamp'])
        c.execute(query, params)

with open('ways_nodes.csv','rb') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        query = 'INSERT INTO ways_nodes VALUES (?, ?, ?);'
        params = (row['id'], row['node_id'], row['position'])
        c.execute(query, params)

with open('ways_tags.csv','rb') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        query = 'INSERT INTO ways_tags VALUES (?, ?, ?, ?);'
        params = (row['id'], row['key'], row['value'], row['type'])
        c.execute(query, params)

print 'Imported CSVs successfully'
print


# close connection
con.commit()
con.close()
