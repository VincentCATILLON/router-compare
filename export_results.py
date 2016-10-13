# encoding: utf-8

import logging
import csv
import pygal

logger = logging.getLogger(__name__)

def _persist_to_box(file_name, data_dict, deviation_type, mode):
    box_plot = pygal.Box()
    box_plot.add('Valhalla', [test["valhalla_{}_deviation_with_google".format(deviation_type)] for test in data_dict])
    box_plot.add('Kraken', [test["kraken_{}_deviation_with_google".format(deviation_type)] for test in data_dict])
    box_plot.title = "{} deviation with Google for the {} mode".format(deviation_type.title(), mode)
    box_plot.render_to_file(file_name)

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
    
    fieldnames = ['id', 'kraken_duration', 'valhalla_duration', 'google_duration']
    _persist_to_csv("test_results/{}_durations.csv".format(mode), results_filtered_by_mode, fieldnames)

    if with_deviation_to_google :
        fieldnames = ['id', 'kraken_duration_deviation_with_google', 'valhalla_duration_deviation_with_google', 'kraken_distance_deviation_with_google', 'valhalla_distance_deviation_with_google']
        _persist_to_csv("test_results/{}_deviations.csv".format(mode), results_filtered_by_mode, fieldnames)


def get_results_as_box_for_a_mode(test_results, mode):
    results_filtered_by_mode = [a_test for a_test in test_results if a_test['mode']==mode]
    _persist_to_box("test_results/{}_durations_deviations.svg".format(mode), results_filtered_by_mode, "duration", mode)
    _persist_to_box("test_results/{}_distances_deviations.svg".format(mode), results_filtered_by_mode, "distance", mode)


if __name__ == '__main__':
    results = [{'to': ['45.77090', '3.08228'], 'valhalla_distance': 1928, 'from': ['45.77316', '3.06115'], 'kraken_duration_deviation_with_google': 290, 'google_distance': 2081, 'valhalla_duration_deviation_with_google': 224, 'google_duration': 1518, 'kraken_distance_deviation_with_google': -57, 'kraken_distance': 2024, 'valhalla_duration': 1742, 'id': '1', 'kraken_duration': 1808, 'mode': 'walking', 'valhalla_distance_deviation_with_google': -153}, {'to': ['45.77090', '3.08228'], 'valhalla_distance': 1934, 'from': ['45.77316', '3.06115'], 'kraken_duration_deviation_with_google':None, 'google_distance': 2497, 'valhalla_duration_deviation_with_google': -12, 'google_duration': 505, 'kraken_distance_deviation_with_google': None, 'kraken_distance': None, 'valhalla_duration': 493, 'id': '2', 'kraken_duration': None, 'mode': 'bicycling', 'valhalla_distance_deviation_with_google': -563}, {'to': ['45.76178338', '3.089832095'], 'valhalla_distance': 3484, 'from':['45.77316', '3.06115'], 'kraken_duration_deviation_with_google': -362, 'google_distance': 3953, 'valhalla_duration_deviation_with_google': -87, 'google_duration': 625, 'kraken_distance_deviation_with_google': -1032, 'kraken_distance': 2921, 'valhalla_duration': 538, 'id': '3', 'kraken_duration': 263, 'mode': 'driving', 'valhalla_distance_deviation_with_google': -469}, {'to': ['45.77836', '3.10326'], 'valhalla_distance': 6437, 'from': ['45.77316', '3.06115'], 'kraken_duration_deviation_with_google': -449, 'google_distance': 4806, 'valhalla_duration_deviation_with_google': -37, 'google_duration': 781, 'kraken_distance_deviation_with_google': -1118, 'kraken_distance': 3688, 'valhalla_duration': 744, 'id': '4', 'kraken_duration': 332, 'mode': 'driving', 'valhalla_distance_deviation_with_google': 1631}, {'to': ['45.779556143', '3.09209346771'], 'valhalla_distance': 774, 'from': ['45.7732405435', '3.09205055237'], 'kraken_duration_deviation_with_google': 86, 'google_distance': 771, 'valhalla_duration_deviation_with_google': 110, 'google_duration': 597, 'kraken_distance_deviation_with_google': -7, 'kraken_distance': 764, 'valhalla_duration': 707, 'id': '5', 'kraken_duration': 683, 'mode': 'walking', 'valhalla_distance_deviation_with_google': 3}, {'to': ['45.778099284', '3.08556741017'], 'valhalla_distance': 379, 'from': ['45.775577', '3.086643'], 'kraken_duration_deviation_with_google': 22, 'google_distance': 390, 'valhalla_duration_deviation_with_google': 30, 'google_duration': 307, 'kraken_distance_deviation_with_google': -22, 'kraken_distance': 368, 'valhalla_duration': 337, 'id': '6', 'kraken_duration': 329, 'mode': 'walking', 'valhalla_distance_deviation_with_google': -11}, {'to': ['45.768523', '3.092028'], 'valhalla_distance': 668, 'from': ['45.7732405435', '3.09205055237'], 'kraken_duration_deviation_with_google': 74, 'google_distance': 673, 'valhalla_duration_deviation_with_google': 87, 'google_duration': 514, 'kraken_distance_deviation_with_google': -15, 'kraken_distance': 658, 'valhalla_duration': 601, 'id': '7', 'kraken_duration': 588, 'mode': 'walking', 'valhalla_distance_deviation_with_google': -5}, {'to': ['45.779556143', '3.09209346771'], 'valhalla_distance': 907, 'from': ['45.7732405435', '3.09205055237'], 'kraken_duration_deviation_with_google': -104, 'google_distance': 996, 'valhalla_duration_deviation_with_google': -40, 'google_duration': 284, 'kraken_distance_deviation_with_google': -259, 'kraken_distance': 737, 'valhalla_duration': 244, 'id': '8', 'kraken_duration': 180, 'mode': 'bicycling', 'valhalla_distance_deviation_with_google': -89}, {'to': ['45.778099284', '3.08556741017'], 'valhalla_distance': 609, 'from': ['45.775577', '3.086643'], 'kraken_duration_deviation_with_google': -102, 'google_distance': 635, 'valhalla_duration_deviation_with_google': 2, 'google_duration': 198, 'kraken_distance_deviation_with_google': -242, 'kraken_distance': 393, 'valhalla_duration': 200, 'id': '9', 'kraken_duration': 96, 'mode': 'bicycling', 'valhalla_distance_deviation_with_google': -26}, {'to': ['45.793835', '3.117304'], 'valhalla_distance': 3025, 'from': ['45.779815', '3.091913'], 'kraken_duration_deviation_with_google': 52, 'google_distance': 2844, 'valhalla_duration_deviation_with_google': 151, 'google_duration': 620, 'kraken_distance_deviation_with_google': -89, 'kraken_distance': 2755, 'valhalla_duration': 771, 'id': '10', 'kraken_duration': 672, 'mode': 'bicycling','valhalla_distance_deviation_with_google': 181}, {'to': ['45.76609419', '3.134926688'], 'valhalla_distance': 5403, 'from': ['45.76178338', '3.089832095'], 'kraken_duration_deviation_with_google': -240, 'google_distance': 4578, 'valhalla_duration_deviation_with_google': 80, 'google_duration': 580, 'kraken_distance_deviation_with_google': -801, 'kraken_distance': 3777, 'valhalla_duration': 660, 'id': '11', 'kraken_duration': 340, 'mode': 'driving', 'valhalla_distance_deviation_with_google': 825}, {'to': ['45.79866639', '3.112698882'], 'valhalla_distance': 37623, 'from': ['45.86091496', '3.543117278'], 'kraken_duration_deviation_with_google': 1529, 'google_distance': 37657, 'valhalla_duration_deviation_with_google': -167, 'google_duration': 1763, 'kraken_distance_deviation_with_google': -1083, 'kraken_distance': 36574, 'valhalla_duration': 1596, 'id': '12', 'kraken_duration': 3292, 'mode': 'driving', 'valhalla_distance_deviation_with_google': -34}]


    #print (results)

    # get_results_as_csv_for_a_mode(results, 'walking')
    # get_results_as_csv_for_a_mode(results, 'driving')
    # get_results_as_csv_for_a_mode(results, 'bicycling')

    get_results_as_box_for_a_mode(results, 'walking')
    get_results_as_box_for_a_mode(results, 'driving')
    get_results_as_box_for_a_mode(results, 'bicycling')
