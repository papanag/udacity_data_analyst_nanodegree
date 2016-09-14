#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
from collections import Counter
import pprint
import re
from tabulate import tabulate


OSMFILE = "boston.osm"



##########   Constants   ##########

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


street_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court",
            "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

street_mapping = { "St": "Street",
            "ST": "Street",
            "St.": "Street",
            "st": "Street",
            "Str": "Street",
            "Sq.": "Square",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "rd.": "Road",
            "Rd": "Road"
            }


postal_expected = ['02108', '02500']

postal_mapping = { "MA": "02108",
            "Mass Ave": "02108",
            "MA 02116": "02116",
            "MA 02118": "02118"
            }


city_expected = ["Boston", "Allston", "Brighton", "Brookline", 
            "Cambridge", "Charlestown", "Somerville"]

city_mapping = { "BOSTON": "Boston",
            "Boston, MA": "Boston",
            "boston": "Boston",
            "Brookline, MA": "Brookline",
            "Cambridge, MA": "Cambridge",
            "Cambridge, Massachusetts": "Cambridge",
            "Roxbury Crossing": "Roxbury",
            "South End": "Boston"
            }


state_expected = ['MA']

state_mapping = { "MA- MASSACHUSETTS": "MA",
            "Ma": "MA",
            "Massachusetts": "MA",
            "ma": "MA"
            }


##########   Audit functions   ##########

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in street_expected:
            street_types[street_type].add(street_name)


def audit_postal_code(invalid_postal_codes, postal_code):
    if not (postal_expected[0] <= postal_code <= postal_expected[1]) \
      or len(postal_code)>5:
        invalid_postal_codes[postal_code] += 1


def audit_city(invalid_cities, city):
    if city not in city_expected:
        invalid_cities[city] += 1


def audit_state(invalid_states, state):
    if state not in state_expected:
        invalid_states[state] += 1


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def is_city(elem):
    return (elem.attrib['k'] == "addr:city")


def is_state(elem):
    return (elem.attrib['k'] == "addr:state")


def key_type(key, keys):
    if lower.search(key):
        keys['lower'] += 1
    elif lower_colon.search(key):
        keys['lower_colon'] += 1
    elif problemchars.search(key):
        keys['problemchars'] += 1
        # pprint.pprint(key)
    else:
        keys['other'] += 1

    return keys


##########   Main function   ##########

def audit(osmfile):
    osm_file = open(osmfile, "r")

    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    key_cnt = Counter()
    street_types = defaultdict(set)
    invalid_postal_codes = defaultdict(lambda:0, {})
    invalid_cities = defaultdict(lambda:0, {})
    invalid_states = defaultdict(lambda:0, {})

    for _, elem in ET.iterparse(osm_file, events=("start",)): 
       if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                key = tag.attrib['k']
                value = tag.attrib['v']

                # audit keys
                keys = key_type(key, keys)

                # count keys
                key_cnt[key] += 1

                # find unexpected street types
                if is_street_name(tag):
                    audit_street_type(street_types, value)

                # find unexpected postal codes
                if is_postal_code(tag):
                    audit_postal_code(invalid_postal_codes, value)

                # find unexpected city names
                if is_city(tag):
                    audit_city(invalid_cities, value)

                # find unexpected state names
                if is_state(tag):
                    audit_state(invalid_states, value)

    osm_file.close()

    print keys
    print

    pprint.pprint(dict(key_cnt))
    print

    street_types_list = []
    for st_type, ways in street_types.iteritems():
        street_types_list.append([st_type, len(ways)])
    pprint.pprint(dict(street_types_list))
    print

    pprint.pprint(dict(invalid_postal_codes))
    print

    pprint.pprint(dict(invalid_cities))
    print

    pprint.pprint(dict(invalid_states))
    print

    return


if __name__ == '__main__':
    audit(OSMFILE)



##########   helper functions for data.py   ##########

def update_street_type(name):
    if name in state_mapping.keys():
        pattern = re.compile('|'.join(street_mapping.keys()))
        name = pattern.sub(lambda x: street_mapping[x.group()], name)

    return name


def update_postal_code(name):
    if name in postal_mapping.keys():
        name = postal_mapping[name]
    elif len(name)>5:
        name = name.split('-')[0]
    
    return name


def update_city(name):
    if name in city_mapping.keys():
        name = city_mapping[name]
    
    return name


def update_state(name):
    if name in state_mapping.keys():
        name = state_mapping[name]
    
    return name





