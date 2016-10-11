# encoding: utf-8

import csv
import connectors as router
import logging


logging.basicConfig(level='DEBUG', format = '%(asctime)s :: %(levelname)s :: %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_test_cases_from_csv_file(csv_file) :
    with open(csv_file,'r') as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        for row in csv_reader:
            #test_case = {"to" : (45.77316,3.06115), "from": (45.77090,3.08228), "mode": "bicycling"}
            test_case = {}
            test_case["from"] = row['origin'].split('/')
            test_case["to"] = row['destination'].split('/')
            test_case["mode"] = row['mode']
            yield test_case


if __name__ == '__main__':

    for a_test_case in get_test_cases_from_csv_file("./test_cases/auvergne.csv"):
        test_router = router.get_distance_and_duration_from_google_directions(a_test_case["from"], a_test_case['to'], a_test_case["mode"])

        if test_router :
            print(">> distance : {} km".format(test_router['distance']/1000.0))
            print(">> durée : {} min".format(test_router['duration']/60.0))
        else :
            print(">> erreur")
