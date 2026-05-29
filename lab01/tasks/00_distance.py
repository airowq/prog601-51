#!/usr/bin/env python3
# -*- coding: utf-8 -*-
sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}
distances = {}
cites = list(sites.keys())
for i in range (len(cites)):
    for j in range (i+1, len(cites)):
        x1, y1 = (sites[cites[i]])
        x2, y2 = (sites[cites[j]])
        dist =  ((x1 - x2)**2 +  (y1 - y2)**2)**0.5
        distances[f'{cites[i]} to {cites[j]}'] = round(dist, 2)
print(distances)
