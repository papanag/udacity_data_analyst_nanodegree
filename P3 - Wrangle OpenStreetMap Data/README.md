# Project 3: Data Wrangling (OpenStreetMap Data Case Study)

### Map Area
Boston, MA, United States

- [http://www.openstreetmap.org/export#map=14/42.3574/-71.0972](http://www.openstreetmap.org/export#map=14/42.3574/-71.0972)
- [http://overpass-api.de/api/map?bbox=-71.1440,42.3365,-71.0505,42.3783](http://overpass-api.de/api/map?bbox=-71.1440,42.3365,-71.0505,42.3783)

This is a map of Boston downtown area. It was selected manually, as openstreetmap.org and mapzen.com preselect the Boston metro area which is huge. This region should have an active community of contributing members on openstreetmap, as there are many universities and tech companies, and thus, we expect to find a variety of points of interest.


## Introduction
First, we downloaded the .osm file for the specified region and we used **osm_sampler.py** to create a smaller but representative file to test with the following scripts. We used **audit.py** to examine tag keys and values of node and way elements. As a result, we identified quite a few problematic cases, like abbreviated street names, wrong zip codes, etc. Using this information, we modified **data.py** to update erroneous entries while building .csv files according to **schema.py**. After that, we imported each .csv file to the corresponding table of a sqlite database by running **db_create.py**. Finally, we chose some interesting queries for our database and we wrote them down in **db_queries.py**.


## Problems Encountered in the Map
Initially, we printed a list of all possible keys and their number of appearances. We selected the most frequent which were eligible for standardization at the same time, so as to clean them programmatically. Specifically, we focused on keys related to address and we found the following problems:

- Abbreviated street names *(“738 Commonwealth Ave”, “Everett St”)*
- Invalid postal codes *(“MA 02116”)*
- Inconsistent city names *(“Brookline, MA”)*
- Malformed state names *(“MA- MASSACHUSETTS”)*

### Abbreviated street names
We used a dictionary with common street types named **street_expected** and checked each street entry. Then, we stored every new occurrence in a dictionary named **street_types**.
```python 
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in street_expected:
            street_types[street_type].add(street_name)
```
In the end, we iterated through the unknown street types, selected those which could be standardized and a mapping for substitutions was created.

### Invalid postal codes
The same method was applied to zip codes. Firstly we defined an acceptable range and then we counted observations exceeding this range.
```python 
def audit_postal_code(invalid_postal_codes, postal_code):
    if not (postal_expected[0] <= postal_code <= postal_expected[1]) \
      or len(postal_code)>5:
        invalid_postal_codes[postal_code] += 1
```
There weren't any incorrect zip codes, only a few missing and a lot concatenated with other parts of the address. Here, we also created a replacement mapping and furthermore, we took note that many entries have a valid first part followed by a dash and other numbers.

### Inconsistent city names
Again, we wrote down a few known city names for the specific region and saved them in a list named **city_expected**. We stored any unknown city names in **invalid_cities**.
```python 
def audit_city(invalid_cities, city):
    if city not in city_expected:
        invalid_cities[city] += 1
```

### Malformed state names
Finally, we audited all state entries and registered anyone different from the official two-letter abbreviation. 
```python 
def audit_state(invalid_states, state):
    if state not in state_expected:
        invalid_states[state] += 1
```

With these four replacement mappings at hand, we introduced functions in **data.py** to update respective fields while constructing the .csv files.


## Data Overview
This section contains basic statistics about the dataset, as also the SQL queries used to gather them.

### File sizes
```
boston.osm ............ 55.5 MB
boston_sample.osm ..... 9.1 MB
osm.sqlite ............ 31 MB
nodes.csv ............. 18.2 MB
nodes_tags.csv ........ 2.5 MB
ways.csv .............. 2.3 MB
ways_tags.csv ......... 3.5 MB
ways_nodes.csv ........ 6.7 MB  
```  

### Number of nodes
```
sqlite> SELECT COUNT(*) FROM nodes;
```
224557

### Number of ways
```
sqlite> SELECT COUNT(*) FROM ways;
```
35702

### Number of unique users
```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
647

### Top 10 contributing users
```sql
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```

```sql
crschmidt           106570
ryebread             32810
wambag               28180
jremillard-massgis   21603
mapper999            12407
morganwahl            6419
OceanVortex           5811
MassGIS Import        3825
JasonWoof             3819
Utible                2111
```
 
### Number of users appearing only once (having 1 post)
```sql
sqlite> SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;
```
178


The contributions of users seem incredibly skewed. Here are some user percentage statistics:
- Top user contribution percentage (“crschmidt”) 40.95%
- Combined Top 5 users contribution 77.45%
- Combined Top 10 users contribution 85.9%
It is worth noting that 2 out of the top ten contributing users have in their username the word “massgis”. This stand for Massachusetts GIS and therefore these may be automated imports from GIS sources.


## Additional Data Exploration

### Top 10 appearing amenities
```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

```sql
bench             319
restaurant        317
bicycle_parking   152
library           134
cafe              130
school             98
bicycle_rental     91
fast_food          90
place_of_worship   90
fountain           60
```
It is impressive that 4 out of the top ten more frequent points of interest are related to a "green" way of life: bench, bicycle_parking, bicycle_rental, fountain. Also, all the other 6 types of amenities are places where people meet up.

### Biggest religion
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;
```
`christian  72`
It is rather unexpected not to find any place of worship besides christian ones.

### Top 10 popular cuisines
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 10;
```

```sql
mexican   18
american  17
pizza     16
italian   15
chinese   14
indian    12
thai      12
asian     10
japanese   9
sandwich   6
```
Here there is a proof for the diversity and multinational identity of Boston. There are equally many restaurants with cuisines from all over around the world.


## Additional ideas for improvement
The best candidate for standardization and automated cleaning is information related to address. Even though we have already cleaned four such fields: street types, zip codes, city names, state name, there is room for improvement. For example, we have found many city names which are numbers. These might be house numbers meddled with the city field. We could try to replace them, but this would require a synthetic approach to mine the correct city name from other available information. On the other hand, it seems an easier task to clean house numbers by stripping any non numerical characters. All in all, this dataset appears to have a quite good level of accuracy, but it could be further improved with cleaning operations as described above.




