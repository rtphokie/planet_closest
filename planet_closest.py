import unittest
from pprint import pprint
from skyfield.api import Loader
from skyfield.searchlib import find_maxima, find_minima
from datetime import datetime

load = Loader('/var/data')
ts = load.timescale()
eph = load('de433.bsp')
# print(eph)
body = None
today = datetime.utcnow()
thisyear = str(today.year)


def closest_planet(planet):
    global body
    distance.step_days = 30  # about a month
    body = eph[planet]

    t1 = ts.utc(1600)
    t2 = ts.utc(2600)
    t, values = find_minima(t1, t2, distance)

    data = {}
    for ti, vi in zip(t, values):
        dt = ti.utc_datetime()
        # print(label, ti.utc_strftime('%Y-%m-%d %H:%M '), f"{vi:,.0f}", 'km')
        data[ti.utc_strftime('%Y-%m-%d')] = vi
    # pprint(data)
    d = data
    this_date = None
    this_distance = None
    since_distance = None
    until_distance = None
    since = None
    until = None
    foundthisyear = False
    for w in sorted(d, key=d.get, reverse=True):
        # print(w, d[w])
        if w.startswith(thisyear):
            foundthisyear = True
            print(w, d[w])
            this_date = w
            this_distance = d[w]
        if foundthisyear and (since is None or until is None):
            year = w[:4]
            if year < thisyear:
                since = w
                since_distance = d[w]
            if year > thisyear:
                until = w
                until_distance = d[w]
    print(since, since_distance)
    print(until, until_distance)
    return this_date, this_distance, since, since_distance, until, until_distance


def distance(t):
    global body
    barycentric = eph['earth'].at(t)
    astrometric = barycentric.observe(body)
    apparent = astrometric.apparent()
    d = apparent.distance()
    return d.km


class MyTestCase(unittest.TestCase):
    def test_something(self):
        for planet in ['Jupiter barycenter']:
            this_date, this_distance, since, since_distance, until, until_distance = closest_planet('jupiter barycenter')
            print(f"{planet.replace(' barycenter', '')} will be {(0.621371*this_distance)/1000000:,.2f} million miles from Earth")
            print(f"this is the closest since {since} ({(0.621371*since_distance)/1000000:,.2f} million miles) {(this_distance-since_distance)*0.621371:,.2f} miles closer")
            print(f"this is the closest until {until} ({(0.621371*until_distance)/1000000:,.2f} million miles) {(this_distance-until_distance)*0.621371:,.2f} miles closer")

    def dtest_something(self):
        global body
        distance.step_days = 30  # about a month
        body = eph['jupiter barycenter']

        t1 = ts.utc(1600)
        t2 = ts.utc(2500)
        t, values = find_minima(t1, t2, distance)

        data = {}
        for ti, vi in zip(t, values):
            dt = ti.utc_datetime()
            # print(label, ti.utc_strftime('%Y-%m-%d %H:%M '), f"{vi:,.0f}", 'km')
            data[ti.utc_strftime('%Y-%m-%d')] = vi
        # pprint(data)
        d = data
        since_distance = None
        until_distance = None
        since = None
        until = None
        foundthisyear = False
        for w in sorted(d, key=d.get, reverse=True):
            # print(w, d[w])
            if w.startswith(thisyear):
                foundthisyear = True
                print(w, d[w])
            if foundthisyear and (since is None or until is None):
                year = w[:4]
                if year < thisyear:
                    since = w
                    since_distance = d[w]
                if year > thisyear:
                    until = w
                    until_distance = d[w]
        print(since, since_distance)
        print(until, until_distance)


if __name__ == '__main__':
    unittest.main()
