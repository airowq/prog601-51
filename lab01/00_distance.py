#!/usr/bin/env python3
# -*- coding: utf-8 -*-
sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}
distances = {}
cities = list(sites.keys())
for i in range (len(cities)):
    for j in range (i+1, len(cities)):
        x1, y1 = (sites[cities[i]])
        x2, y2 = (sites[cities[j]])
        dist =  ((x1 - x2)**2 +  (y1 - y2)**2)**0.5
        distances[f'{cities[i]} to {cities[j]}'] = round(dist, 2)
print(distances)