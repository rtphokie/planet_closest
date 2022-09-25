import unittest
from pprint import pprint
from skyfield.api import Loader
from skyfield.searchlib import find_maxima, find_minima
from datetime import datetime

load = Loader('/var/data')
ts = load.timescale()
eph = load('de431t.bsp')
body = None
today = datetime.utcnow()
thisyear = str(today.year)


def closest_planet(planet):
    global body
    distance.step_days = 30  # about a month
    body = eph[planet]

    t1 = ts.utc(999)
    t2 = ts.utc(9999)
    t, values = find_minima(t1, t2, distance)

    data = {}
    for ti, vi in zip(t, values):
        data[ti.utc_strftime('%Y-%m-%d')] = vi
    d = data
    this_date = None
    this_distance = None
    since_distance = None
    until_distance = None
    since = None
    until = None
    foundthisyear = False
    for w in sorted(d, key=d.get, reverse=True):
        if w.startswith(thisyear):
            foundthisyear = True
            this_date = w
            this_distance = d[w]
        if foundthisyear and (since is None or until is None):
            year = w[:4]
            if year < thisyear and since is None:
                since = w
                since_distance = d[w]
            if year > thisyear and until is None:
                until = w
                until_distance = d[w]
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
        for planet in ['Mercury', 'Venus', 'Mars barycenter', 'Jupiter barycenter', 'Saturn barycenter']:
            this_date, this_distance, since, since_distance, until, until_distance = closest_planet(planet)
            print(
                f"{planet.replace(' barycenter', '')} will be {(0.621371 * this_distance) / 1000000:,.2f} million miles from Earth on {this_date}")
            print(
                f"this is the closest since {since} ({(0.621371 * since_distance) / 1000000:,.2f} million miles) {(this_distance - since_distance) * 0.621371:,.2f} miles closer")
            print(
                f"this is the closest until {until} ({(0.621371 * until_distance) / 1000000:,.2f} million miles) {(this_distance - until_distance) * 0.621371:,.2f} miles closer")
            print()


if __name__ == '__main__':
    unittest.main()
