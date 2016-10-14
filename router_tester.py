# encoding: utf-8

import csv
import logging
import connectors as router
import export_results as export


logging.basicConfig(level='DEBUG', format = '%(asctime)s :: %(levelname)s :: %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def get_test_cases_from_csv_file(csv_file) :
    with open(csv_file,'r') as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        for row in csv_reader:
            #test_case = {"to" : (45.77316,3.06115), "from": (45.77090,3.08228), "mode": "bicycling"}
            test_case = {}
            test_case["from"] = row['origin'].split('/')
            test_case["to"] = row['destination'].split('/')
            test_case["mode"] = row['mode']
            test_case["id"] = row['id']
            yield test_case

def add_deviation_to_google(result_list) :
    logger.info("Calcul des différences de distances et de durée en prenant google comme référence")
    result_list = [dict({'kraken_distance_deviation_with_google' : 100 * (a_test_result["kraken_distance"] - a_test_result["google_distance"]) /a_test_result["google_distance"]}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'kraken_duration_deviation_with_google' : 100 * (a_test_result["kraken_duration"] - a_test_result["google_duration"]) / a_test_result["google_duration"]}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'valhalla_distance_deviation_with_google' : 100 * (a_test_result["valhalla_distance"] - a_test_result["google_distance"]) /a_test_result["google_distance"]}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'valhalla_duration_deviation_with_google' : 100 * (a_test_result["valhalla_duration"] - a_test_result["google_duration"]) / a_test_result["google_duration"]}, **a_test_result) for a_test_result in result_list]
    return result_list

def remove_not_consistent_test_retults(result_list) :
    logger.info("Suppression des résultats de tests pour lesquels des valeurs sont manquantes")
    result_list = [a_test_result for a_test_result in result_list if a_test_result["kraken_duration"] and a_test_result["valhalla_duration"] and a_test_result["google_duration"]]
    return result_list

def order_test_results(result_list, order_criteria) :
    logger.info("Tri des résultats par distance à vol d'oiseau")
    return sorted(result_list, key=lambda result: float(result[order_criteria]))

if __name__ == '__main__':
    test_result_list = []

    for a_test_case in get_test_cases_from_csv_file("./test_cases/auvergne.csv"):
        test_result = dict(a_test_case)
        logger.info("Test en cours sur l'élément " + a_test_case['id'])
        test_router_kraken = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"])
        test_router_valhalla = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"], additionnal_params={"_override_scenario": "experimental"})
        test_router_google = router.get_distance_and_duration_from_google_directions(a_test_case["from"], a_test_case['to'], a_test_case["mode"])
        test_router_superman = router.get_crow_fly_distance(a_test_case["from"], a_test_case['to'])

        if test_router_kraken :
            test_result["kraken_distance"] = test_router_kraken['distance']
            test_result["kraken_duration"] = test_router_kraken['duration']
        else :
            test_result["kraken_distance"] = test_result["kraken_duration"] = None

        if test_router_valhalla :
            test_result["valhalla_distance"] = test_router_valhalla['distance']
            test_result["valhalla_duration"] = test_router_valhalla['duration']
        else :
            test_result["valhalla_distance"] = test_result["valhalla_duration"] = None

        if test_router_google :
            test_result["google_distance"] = test_router_google['distance']
            test_result["google_duration"] = test_router_google['duration']
        else :
            test_result["google_distance"] = test_result["google_duration"] = None

        test_result["superman_distance"] = test_router_superman['distance']

        test_result_list.append(test_result)


    test_result_list = order_test_results(test_result_list, "superman_distance")

    export.get_results_as_csv_for_a_mode(test_result_list, 'walking')
    export.get_results_as_csv_for_a_mode(test_result_list, 'driving')
    export.get_results_as_csv_for_a_mode(test_result_list, 'bicycling')

    test_result_list = remove_not_consistent_test_retults(test_result_list)
    test_result_list = add_deviation_to_google(test_result_list)

    export.get_results_as_box_for_a_mode(test_result_list, 'walking')
    export.get_results_as_box_for_a_mode(test_result_list, 'driving')
    export.get_results_as_box_for_a_mode(test_result_list, 'bicycling')
