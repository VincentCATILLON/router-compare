# encoding: utf-8

import json
import requests
import logging
import auth_params

GOOGLE_TOKEN = auth_params.google_api_key

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

    url_params = {"origin": origin, "destination" : destination, "mode" : mode, "key": GOOGLE_TOKEN}
    url = "https://maps.googleapis.com/maps/api/directions/json"
    call = requests.get(url, params = url_params)
    logger.debug(call.url)
    if call.status_code != 200 :
        logger.error("Appel à l'API Google KO - status code : {}".format(call.status_code))
        return
    google_response = call.json()
    if google_response['status'] != "OK" :
        logger.error("Appel à l'API Google KO - message : {}".format(google_response['status']))
        return

    return {'distance' : google_response['routes'][0]['legs'][0]['distance']['value'], 'duration': google_response['routes'][0]['legs'][0]['duration']['value']}
