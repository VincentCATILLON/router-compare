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

def get_results_as_csv_for_a_mode(test_results, mode):
    logger.info("Génération de fichiers csv avec les résultats des tests pour le mode " + mode)
    results_filtered_by_mode = [a_test for a_test in test_results if a_test['mode']==mode]

    fieldnames = ['id', 'kraken_distance', 'valhalla_distance', 'google_distance']
    _persist_to_csv("test_results/{}_distances.csv".format(mode), results_filtered_by_mode, fieldnames)

    fieldnames = ['id', 'kraken_duration', 'valhalla_duration', 'google_duration']
    _persist_to_csv("test_results/{}_durations.csv".format(mode), results_filtered_by_mode, fieldnames)


def get_results_as_box_for_a_mode(test_results, mode):
    results_filtered_by_mode = [a_test for a_test in test_results if a_test['mode']==mode]
    _persist_to_box("test_results/{}_durations_deviations.svg".format(mode), results_filtered_by_mode, "duration", mode)
    _persist_to_box("test_results/{}_distances_deviations.svg".format(mode), results_filtered_by_mode, "distance", mode)
