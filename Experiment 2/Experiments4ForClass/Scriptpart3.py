import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import re
import json

prefix_df = pd.read_csv(r'prefix_lat_lon_name_category.csv')
df = pd.read_csv(r'outputwireless-logs-20120409.DHCP_ANON.csv')

mapping = dict()
for index, row in prefix_df.iterrows():
    mapping[row['prefix']] = row['name']

peopleLocs = defaultdict(Counter)
people = defaultdict(Counter)
building = defaultdict(Counter)
building_tot = Counter()
for index, row in df.iterrows():
    locargs = row['APNAME'].split('-')
    locap = locargs[0]
    knownMatch = re.match(r'([A-Za-z]+)(?:\w+)*$', locap)
    location = locap
    if knownMatch:
        prefix = knownMatch.group(1)
        if prefix in mapping:
            location = prefix
    dt = datetime.utcfromtimestamp(row['startTime'])

    # morning (5am <= m < 11am)
    # lunch (11am <= l < 4pm)
    day = 'evening'
    if 5 <= dt.hour < 11:
        day = 'morning'
    elif 11 <= dt.hour < 16:
        day = 'lunch'

    uid = row['userMAC']
    peopleLocs[uid][location] += 1
    people[uid][day] += 1
    building[day][location] += 1
    building_tot[location] += 1
# classify into bins (morning, lunch, evening)
types = defaultdict(list)
for uid in people:
    data = people[uid]
    typeOfPerson = (None, 0)
    for day in data:
        if data[day] > typeOfPerson[1]:
            typeOfPerson = (day, data[day])
    types[typeOfPerson[0]].append(uid)
with open('classified.txt', 'w') as outfile:
    json.dump(types, outfile)
# which buildings are popular certain times of the day
plt.figure(figsize=(50, 10))
buildings = [loc for loc, val in sorted(
    mapping.items(), key=lambda item: item[0] in building_tot and building_tot[item[0]] or 0, reverse=True)]
index = 0
width = 0.25
for day in building:
    y = []
    for prefix in buildings:
        y.append(building[day][prefix])
    ind = np.arange(len(buildings))
    plt.bar(ind + width * index, y, width=width, label=day)
    plt.ylabel('Frequency')
    plt.xlabel('Buildings', rotation=90)
    plt.yticks(rotation=90, va="center", ha="right")
    plt.xticks(ind + width, buildings, rotation=90, va="top", ha="center")
    plt.legend()
    index += 1
plt.tight_layout()
plt.savefig("buildingpopular")
# which buildings are more popular are among the types of people
for t in types:
    plt.figure(figsize=(100, 10))
    people = types[t]
    yp = Counter()
    for uid in people:
        for prefix in buildings:
            yp[prefix] += peopleLocs[uid][prefix]
    y = yp.values()
    plt.bar(buildings, y)
    plt.ylabel('Frequency')
    plt.xlabel('Buildings', rotation=90)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(t)