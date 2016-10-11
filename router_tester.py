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
        print("----- {} ".format(a_test_case))
        test_router_kraken = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"])
        test_router_valhalla = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"], additionnal_params= {"_override_scenario": "experimental"})
        test_router_google = router.get_distance_and_duration_from_google_directions(a_test_case["from"], a_test_case['to'], a_test_case["mode"])

        if test_router_kraken :
            print(">> distance kraken : {} km".format(test_router_kraken['distance']/1000.0))
            print(">> durée kraken : {} min".format(test_router_kraken['duration']/60.0))
        else :
            print(">> erreur pour kraken")

        if test_router_valhalla :
            print(">> distance valhalla : {} km".format(test_router_valhalla['distance']/1000.0))
            print(">> durée valhalla : {} min".format(test_router_valhalla['duration']/60.0))
        else :
            print(">> erreur pour valhalla")

        if test_router_google :
            print(">> distance google : {} km".format(test_router_google['distance']/1000.0))
            print(">> durée google : {} min".format(test_router_google['duration']/60.0))
        else :
            print(">> erreur pour google")
