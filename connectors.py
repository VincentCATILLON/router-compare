# encoding: utf-8

import json
import requests
import logging

def get_distance_and_duration_from_google_directions(from_tuple, to_tuple, mode):
    """
    Uses google directions API to compute journey and extract duration & distance
    """
    logger = logging.getLogger(__name__)
    if mode not in ("walking", "bicycling", "driving"):
        logger.error("Le mode {} est inconnu - valeurs acceptées : walking, biking, driving".format(mode))
        return

    origin = "{},{}".format(from_tuple[0], from_tuple[1])
    destination = "{},{}".format(to_tuple[0], to_tuple[1])

    url = "http://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&mode={}".format(origin, destination, mode)
    logger.debug(url)
    call = requests.get(url)
    if call.status_code != 200 :
        logger.error("Appel à l'API Google KO - status code : {}".format(call.status_code))
        return
    google_response = call.json()
    if google_response['status'] != "OK" :
        logger.error("Appel à l'API Google KO - message : {}".format(google_response['status']))
        return

    return {'distance' : google_response['routes'][0]['legs'][0]['distance']['value'], 'duration': google_response['routes'][0]['legs'][0]['duration']['value']}

if __name__ == '__main__':

    from_ = (48.75139,2.50588)
    to_ = (48.9771,3.0924)
    #to_ = (3.0924,566)
    test_router = get_distance_and_duration_from_google_directions(from_, to_, mode = "driving")

    if test_router :
        print("distance : {} km".format(test_router['distance']/1000.0))
        print("durée : {} min".format(test_router['duration']/60.0))
    else :
        print("erreur")
