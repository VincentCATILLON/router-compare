# encoding: utf-8

import csv
import connectors as router
import logging


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

def _persist_to_csv(file_name, data_dict, data_headers):
    result_to_persist = [ dict((k, result.get(k, None)) for k in data_headers) for result in data_dict]
    with open(file_name, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_headers, delimiter=';')
        writer.writeheader()
        for a_row in result_to_persist:
            writer.writerow(a_row)

def get_results_as_csv_for_a_mode(test_results, mode, with_deviation_to_google = False):
    logger.info("Génération de fichiers csv avec les résultats des tests pour le mode " + mode)
    results_filtered_by_mode = [a_test for a_test in test_results if a_test['mode']==mode]

    fieldnames = ['id', 'kraken_distance', 'valhalla_distance', 'google_distance']
    _persist_to_csv("test_results/{}_distances.csv".format(mode), results_filtered_by_mode, fieldnames)

    if with_deviation_to_google :
        fieldnames = ['id', 'kraken_duration', 'valhalla_duration', 'google_duration']
        _persist_to_csv("test_results/{}_durations.csv".format(mode), results_filtered_by_mode, fieldnames)

        fieldnames = ['id', 'kraken_duration_deviation_with_google', 'valhalla_duration_deviation_with_google', 'kraken_distance_deviation_with_google', 'valhalla_distance_deviation_with_google']
        _persist_to_csv("test_results/{}_deviations.csv".format(mode), results_filtered_by_mode, fieldnames)


def soustract_me_if_you_can(one, two) :
    if one and two :
        return one - two

def add_deviation_to_google(result_list) :
    logger.info("Calcul des différences de distances et de durée en prenant google comme référence")
    result_list = [dict({'kraken_distance_deviation_with_google' : soustract_me_if_you_can(a_test_result["kraken_distance"], a_test_result["google_distance"])}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'kraken_duration_deviation_with_google' : soustract_me_if_you_can(a_test_result["kraken_duration"], a_test_result["google_duration"])}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'valhalla_distance_deviation_with_google' : soustract_me_if_you_can(a_test_result["valhalla_distance"], a_test_result["google_distance"])}, **a_test_result) for a_test_result in result_list]
    result_list = [dict({'valhalla_duration_deviation_with_google' : soustract_me_if_you_can(a_test_result["valhalla_duration"], a_test_result["google_duration"])}, **a_test_result) for a_test_result in result_list]
    return result_list



if __name__ == '__main__':
    test_result_list = []

    for a_test_case in get_test_cases_from_csv_file("./test_cases/auvergne.csv"):
        test_result = dict(a_test_case)
        print("----- ")
        test_router_kraken = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"])
        test_router_valhalla = router.get_distance_and_duration_from_navitia(a_test_case["from"], a_test_case['to'], a_test_case["mode"], additionnal_params={"_override_scenario": "experimental"})
        test_router_google = router.get_distance_and_duration_from_google_directions(a_test_case["from"], a_test_case['to'], a_test_case["mode"])

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

        test_result_list.append(test_result)

    test_result_list = add_deviation_to_google(test_result_list)

    get_results_as_csv_for_a_mode(test_result_list, 'walking', with_deviation_to_google = True)
    get_results_as_csv_for_a_mode(test_result_list, 'driving', with_deviation_to_google = True)
    get_results_as_csv_for_a_mode(test_result_list, 'bicycling', with_deviation_to_google = True)
