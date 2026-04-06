#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# в саду сорвали цветы
garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза', )

# на лугу сорвали цветы
meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка', )

# создайте множество цветов, произрастающих в саду и на лугу
# garden_set =
# meadow_set =
# TODO здесь ваш код
garden_set = list(set([x for x in garden]))
meadow_set = list(set([x for x in meadow]))
# выведите на консоль все виды цветов
# TODO здесь ваш код
print(list(set(meadow_set+garden_set)))
# выведите на консоль те, которые растут и там и там
# TODO здесь ваш код
print([x for x in meadow_set if x in garden_set])
# выведите на консоль те, которые растут в саду, но не растут на лугу
# TODO здесь ваш код
print([x for x in garden_set if not(x in meadow_set)])
# выведите на консоль те, которые растут на лугу, но не растут в саду
# TODO здесь ваш код
print([x for x in meadow_set if not(x in garden_set)])