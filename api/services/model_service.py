from dataclasses import dataclass
import os
from csv import reader, DictWriter
from unittest import result
# import requests
from base_logger import logger
from  geopy.distance import geodesic 
import pandas as pd
from flask import  abort, jsonify
import numpy as np
import json
import joblib

def main(data):
    """
    Orchestrates the transformation of the received data and uses the model to return the predicted price.

    :return:
    """
    # post shcema
    # data = {
        # "host_id":3159,
        # "listing_info":{
        #     "latitude":52.36435,
        #     "longitude":4.94358,
        #     "room_type":"Private room",
        #     "minimum_nights":3,
        #     "maximum_nights":15,
        #     "accomodates": 2,
        #     "neighbouhood": "ΓΚΥΖΙ",
        #     "property_type": "Room in boutique hotel",
        #     "bathrooms": 1,
        #     "shared_bathroom":False,
        #     "has_availability":True,
        #     "license":True, 
        #     "instant_bookable": True
        #     },
        # "amenities": {
        #     'kitchen':True,
        #     'air_conditioning':False,
        #     'high_end_electronics':True,
        #     'bbq':False,
        #     'balcony': True,
        #     'nature_and_views':False,
        #     'bed_linen':True,
        #     'breakfast':False,
        #     'tv':True,
        #     'coffee_machine':False,
        #     'cooking_basics':False,
        #     'elevator':True, 
        #     'gym':False, 
        #     'child_friendly':True, 
        #     'parking':False,
        #     'outdoor_space':False,
        #     'host_greeting':False, 
        #     'hot_tub_sauna_or_pool':False,
        #     'internet':True, 
        #     'long_term_stays':True,
        #     'pets_allowed':False,
        #     'private_entrance':False,
        #     'secure':True, 
        #     'self_check_in':True,
        #     'smoking_allowed':False,
        #     'accessible': True, 
        #     'event_suitable':False,
        #     "tv": True,
        #     "kitchen":False,
        #     "air_conditioning": True
        #     }
        #   }
    #resultset = [value for key, value in your_dict.items() if key not in your_blacklisted_set]
    try:
        final_data = preprocess_dataset(data)
        price = get_price(final_data)

        info_to_return = {
            "host_id": data['host_id'],
            "number_of_reviews": final_data['number_of_reviews'],
            "neighbourhood": data['listing_info']['neighbourhood'],
            "room_type": data['listing_info']['room_type']
        }

        return {'listing_info': info_to_return, 'prediction': {'price': price}}
    
    except Exception as exception:
        logger.error(f"Could not predict price {exception}")
        return None


def preprocess_dataset(data):

    host_info = get_host_info(data['host_id'])

    # Error handling for the existance of the listing in our repo
    if not host_info:
        return None
    elif 'error' in host_info:
        return host_info

    try:
        listing_info = missing_values_n_encoding(data['listing_info'])
        amenities = get_amenities(data['amenities'])
        final_data = pd.concat([listing_info, amenities, host_info])
        # logger.error(data)
        return final_data
    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")

def get_amenities(amenities_data):
    amenities = pd.DataFrame.from_dict(amenities_data, orient='index')
    amenities.reset_index(inplace=True, drop=True)
    amenities = amenities.astype(int)
    amenities["amenities_number"]=amenities.sum(axis=1)
    return amenities

def missing_values_n_encoding(listing_info):

    #     'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type',
    #     'room_type', 'accommodates','minimum_nights', 'maximum_nights',
    #     'availability_90', 'number_of_reviews', 'bathrooms']


    with open(os.getcwd() + "/api/repo/neighbourhood_groupings.json", "r") as read_content:
        neigh_group = json.load(read_content)

    listing_info = pd.DataFrame.from_dict(listing_info, orient='index')
    listing_info.reset_index(inplace=True, drop=True)
    
    listing_info['lat_center'] = 37.9715
    listing_info['lon_center'] = 23.7257
    listing_info['neighbourhood_cleansed_group'] = listing_info['neighbourhood_cleansed'].map(neigh_group)
    listing_info['distance_parthenon'] = listing_info.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    listing_info = listing_info.drop(columns=['lat_center','lon_center'])

    listing_info['shared_bathroom'] = listing_info['shared_bathroom'].astype(int)
    listing_info['has_availability'] = listing_info['has_availability'].astype(int)
    listing_info['license'] = listing_info['license'].astype(int)
    listing_info['instant_bookable'] = listing_info['instant_bookable'].astype(int)
    return listing_info


def get_price(data):
    loaded_model = joblib.load(os.getcwd() + "/api/repo/pipeline.pkl")
    price = loaded_model.predict(data)
    return price

def get_host_info(host_id):
    

    # list_ask = ['host_about', 'host_response_time', 'host_response_rate',
    #    'host_is_superhost', 'host_verifications', 
    #    'calculated_host_listings_count']


    # info_all = pd.read_csv(os.getcwd() + "/api/repo/listings_info.csv")
    # info = {}
    # info_id = info_all[info_all['id'] == host_id]
    # if info_id.shape[0] == 1:
    #     info['neighbourhood'] = info_id['neighbourhood_cleansed'].item()
    #     info['reviews_per_month'] = info_id['reviews_per_month'].item()
    #     info['room_type'] = info_id['room_type'].item()
    #     return info
    # elif info_id.shape[0] > 1:
    #     logger.error(f"Internal error, too many listings with same id")
    #     return {'error':'too many listings'}
    # else:
    #     logger.error("No listing with id: {} exist".format(listing_id))
    #     return None

    #TODO make a host info csv and extract from it all info necessary 
    pass
        