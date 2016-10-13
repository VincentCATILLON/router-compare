# encoding: utf-8

import json
import requests
import logging
import math
import auth_params

GOOGLE_TOKEN = auth_params.google_api_key
NAVITIA_TOKEN = auth_params.navitia_api_key
NAVITIA_URL = auth_params.navitia_base_url

mode_mapping = {"walking": "walking", "driving" : "car", "bicycling": "bike"}

logger = logging.getLogger(__name__)


def mode_is_valid(mode_candidate):
    return mode_candidate in mode_mapping


def get_distance_and_duration_from_navitia(from_tuple, to_tuple, mode, coverage="fr-auv", additionnal_params={}):
    """
    Call navitia to compute a non pt journey and extract duration & distance from the appropriate section
    """
    if not mode_is_valid(mode):
        logger.error("Le mode {} est inconnu - valeurs acceptées : walking, biking, driving".format(mode))
        return

    fallback_mode = mode_mapping[mode]
    origin = "{};{}".format(from_tuple[1], from_tuple[0])
    destination = "{};{}".format(to_tuple[1], to_tuple[0])

    url_params = {"from" : origin, "to": destination, "first_section_mode[]": fallback_mode, "last_section_mode[]" : fallback_mode}
    url_params["max_duration"] = 0 #force non PT journey
    url_params["count"] = 1
    url_params = dict(url_params, **additionnal_params)

    url = NAVITIA_URL + "/coverage/{}/journeys".format(coverage)
    call = requests.get(url, params=url_params,  headers={'Authorization': NAVITIA_TOKEN})
    logger.debug(call.url)
    if not call.status_code == 200 :
        logger.error("Appel à navitia KO - status code : {}".format(call.status_code))
        return
    navitia_response = call.json()
    if not "journeys" in navitia_response :
        logger.error("Pas d'itinéraire retourné par navitia : " + navitia_response["error"]["message"])
        return
    navitia_journey = navitia_response['journeys'][0]
    if not "non_pt" in navitia_journey['tags'] :
        logger.error("L'itinéraire retourné par navitia n'est pas exploitable (contient du transport en commun)")
        return
    if not navitia_journey["sections"][0]["mode"] == fallback_mode :
        logger.error("L'itinéraire retourné par navitia n'est pas exploitable (le mode trouvé ne concorde pas)")
        return

    return {'distance' : navitia_journey["sections"][0]["geojson"]["properties"][0]["length"], 'duration': navitia_journey["sections"][0]["duration"]}

def get_distance_and_duration_from_google_directions(from_tuple, to_tuple, mode):
    """
    Uses google directions API to compute journey and extract duration & distance
    """

    if not mode_is_valid(mode):
        logger.error("Le mode {} est inconnu - valeurs acceptées : walking, biking, driving".format(mode))
        return

    origin = "{},{}".format(from_tuple[0], from_tuple[1])
    destination = "{},{}".format(to_tuple[0], to_tuple[1])

    url_params = {"origin": origin, "destination" : destination, "mode" : mode, "key": GOOGLE_TOKEN}
    url = "https://maps.googleapis.com/maps/api/directions/json"
    call = requests.get(url, params=url_params)
    logger.debug(call.url)
    if call.status_code != 200 :
        logger.error("Appel à l'API Google KO - status code : {}".format(call.status_code))
        return
    google_response = call.json()
    if google_response['status'] != "OK" :
        logger.error("Appel à l'API Google KO - message : {}".format(google_response['status']))
        return

    return {'distance' : google_response['routes'][0]['legs'][0]['distance']['value'], 'duration': google_response['routes'][0]['legs'][0]['duration']['value']}

def get_crow_fly_distance(from_tuple,to_tuple):
    lat1, lon1 = from_tuple
    lat2, lon2 = to_tuple

    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)

    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return {'distance' : d}
