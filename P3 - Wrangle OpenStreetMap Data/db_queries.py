import sqlite3
import os
from tabulate import tabulate

# open database
def open_db(filename):
    file_exists = os.path.isfile(filename)
    if file_exists == False:
        print ''' "{}" database not found '''.format(filename)
        exit()
    print ''' "{}" database successfully opened '''.format(filename)
    con = sqlite3.connect(filename)
    return con

con = open_db('osm.sqlite')
c = con.cursor()


# make queries
query = '''SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode'
GROUP BY tags.value
ORDER BY count DESC;'''
c.execute(query)
print '\n', 'Postal Codes:'
print tabulate(c.fetchall())


query = '''SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;'''
c.execute(query)
print '\n', 'Sort cities by count:'
print tabulate(c.fetchall())


query = 'SELECT COUNT(*) FROM nodes;'
c.execute(query)
print '\n', 'Number of nodes:', c.fetchone()[0]


query = 'SELECT COUNT(*) FROM ways;'
c.execute(query)
print '\n', 'Number of ways:', c.fetchone()[0]


query = '''SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;'''
c.execute(query)
print '\n', 'Number of unique users:', c.fetchone()[0]


query = '''SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes 
      UNION ALL 
      SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;'''
c.execute(query)
print '\n', 'Top 10 contributing users:'
print tabulate(c.fetchall())


query = '''SELECT COUNT(*) 
FROM (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes 
           UNION ALL 
           SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1) u;'''
c.execute(query)
print '\n', 'Number of users appearing only once:'
print tabulate(c.fetchall())


query = '''SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;'''
c.execute(query)
print '\n', 'Top 10 appearing amenities:'
print tabulate(c.fetchall())


query = '''SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
JOIN (SELECT DISTINCT(id) FROM nodes_tags 
      WHERE value='place_of_worship') i
ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;'''
c.execute(query)
print '\n', 'Biggest religion:'
print tabulate(c.fetchall())


query = '''SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
JOIN (SELECT DISTINCT(id) FROM nodes_tags 
      WHERE value='restaurant') i
ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 10;'''
c.execute(query)
print '\n', 'Most popular cuisines:'
print tabulate(c.fetchall())




# close connection
con.commit()
con.close()
