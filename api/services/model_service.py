from dataclasses import dataclass
import os
from csv import reader, DictWriter
from unittest import result
# import requests
from base_logger import logger
from geopy.distance import geodesic
import pandas as pd
from flask import abort, jsonify
import numpy as np
import json
import joblib
import xgboost as xgb
import pickle

def main(data):
    """
    Orchestrates the transformation of the received data and uses the model to return the predicted price.

    :return:
    """
    # post shcema
    # postman
    # {
    #     "host_id": 3159,
    #     "listing_info": {
    #         "latitude": 52.36435,
    #         "longitude": 4.94358,
    #         "room_type": "Private room",
    #         "minimum_nights": 3,
    #         "maximum_nights": 15,
    #         "accomodates": 2,
    #         "neighbourhood": "ΓΚΥΖΗ",
    #         "property_type": "Room in boutique hotel",
    #         "bathrooms": 1,
    #         "shared_bathroom": false,
    #         "has_availability": true,
    #         "license": true,
    #         "instant_bookable": true,
    #         "number_of_reviews": 10
    #     },
    #     "amenities": {
    #         "kitchen": true,
    #         "air_conditioning": false,
    #         "high_end_electronics": true,
    #         "bbq": false,
    #         "balcony": true,
    #         "nature_and_views": false,
    #         "bed_linen": true,
    #         "breakfast": false,
    #         "tv": true,
    #         "coffee_machine": false,
    #         "cooking_basics": false,
    #         "elevator": true,
    #         "gym": false,
    #         "child_friendly": true,
    #         "parking": false,
    #         "outdoor_space": false,
    #         "host_greeting": false,
    #         "hot_tub_sauna_or_pool": false,
    #         "internet": true,
    #         "long_term_stays": true,
    #         "pets_allowed": false,
    #         "private_entrance": false,
    #         "secure": true,
    #         "self_check_in": true,
    #         "smoking_allowed": true,
    #         "accessible": true,
    #         "event_suitable": true
    #     }
    # }

    #resultset = [value for key, value in your_dict.items() if key not in your_blacklisted_set]
    # logger.error(f"Could not predict price {data}")
    try:
        final_data = preprocess_dataset(data)
        price = get_price(final_data)

        info_to_return = {
            "host_id": int(data['host_id']),
            "number_of_reviews": int(final_data['number_of_reviews'].iloc[0]),
            "neighbourhood_cleansed": data['listing_info']['neighbourhood_cleansed'],
            "room_type": data['listing_info']['room_type']
        }

        return {'listing_info': info_to_return, 'prediction': {'price': int(price)}}
    
    except Exception as exception:
        logger.error(f"Could not predict price {exception}")
        return None


def preprocess_dataset(data):

    # host_info = get_host_info(data['host_id'])

    # Error handling for the existance of the listing in our repo
    # if not host_info:
    #     return None
    # elif 'error' in host_info:
    #     return host_info

    try:
        listing_info = missing_values_n_encoding(data['listing_info'])

        amenities = get_amenities(data['amenities'])

        host_info = get_host_info(data['host_id'])

        final_data = pd.concat([host_info, listing_info, amenities], axis=1,ignore_index=False)

        logger.error(final_data)

        # final_data = final_data.reindex(columns=['host_about', 'host_response_time', 'host_response_rate', 'host_is_superhost',
        #                          'host_verifications', 'host_has_profile_pic', 'host_identity_verified',
        #                          'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type', 'room_type',
        #                          'accommodates', 'minimum_nights', 'maximum_nights', 'has_availability',
        #                          'availability_90', 'number_of_reviews', 'license', 'instant_bookable',
        #                          'calculated_host_listings_count', 'kitchen', 'air_conditioning',
        #                          'high_end_electronics', 'bbq', 'balcony', 'nature_and_views', 'bed_linen', 'breakfast',
        #                          'tv', 'coffee_machine', 'cooking_basics', 'elevator', 'gym', 'child_friendly',
        #                          'parking', 'outdoor_space', 'host_greeting', 'hot_tub_sauna_or_pool', 'internet',
        #                          'long_term_stays', 'pets_allowed', 'private_entrance', 'secure', 'self_check_in',
        #                          'smoking_allowed', 'accessible', 'event_suitable', 'neighbourhood_cleansed_group',
        #                          'amenities_number', 'distance_parthenon', 'shared_bath', 'bathrooms'])
        # logger.error(final_data.shape)

        final_data.to_csv(os.getcwd() +'/test.csv')
        return final_data
    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")

def get_amenities(amenities_data):
    amenities = pd.DataFrame.from_dict({"amen": amenities_data}, orient='index')
    amenities.reset_index(inplace=True, drop=True)
    amenities = amenities.astype(int)
    amenities["amenities_number"] = amenities.sum(axis=1)
    # logger.error(amenities)
    return amenities

def missing_values_n_encoding(listing_info):

    #     'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type',
    #     'room_type', 'accommodates','minimum_nights', 'maximum_nights',
    #     'availability_90', 'number_of_reviews', 'bathrooms']

    # logger.error(listing_info)
    with open(os.getcwd() + "/repo/neighbourhood_groupings.json", "r", encoding="utf8") as read_content:
        neigh_group = json.load(read_content)

    listing_info = pd.DataFrame.from_dict({"info": listing_info}, orient='index')
    # , orient = 'index'
    listing_info.reset_index(inplace=True, drop=True)


    listing_info['lat_center'] = 37.9715
    listing_info['lon_center'] = 23.7257
    listing_info['neighbourhood_cleansed_group'] = listing_info['neighbourhood_cleansed'].map(neigh_group)
    listing_info['distance_parthenon'] = listing_info.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    listing_info = listing_info.drop(columns=['lat_center','lon_center'])

    listing_info['shared_bath'] = listing_info['shared_bath'].astype(int)
    listing_info['has_availability'] = listing_info['has_availability'].astype(int)
    listing_info['license'] = listing_info['license'].astype(int)
    listing_info['instant_bookable'] = listing_info['instant_bookable'].astype(int)

    # logger.error(listing_info['neighbourhood_cleansed_group'])
    # logger.error(listing_info['distance_parthenon'])
    # logger.error(listing_info['shared_bath'])
    # logger.error(listing_info['has_availability'])
    # logger.error(listing_info['license'])
    # logger.error(listing_info['instant_bookable'])




    # logger.error(listing_info['neighbourhood_group'])
    return listing_info


def get_price(data):
    # logger.error(data)
    # booster = xgb.Booster()
    loaded_model = joblib.load(os.getcwd() + "/repo/pipeline.pkl")

    # loaded_transformer = joblib.load(os.getcwd() + "/repo/transformerVectorizer.pkl")
    # loaded_model = joblib.load(os.getcwd() + "/repo/xgbRegressor.pkl")

    # logger.error(data)
    price = loaded_model.predict(data)
    # price = 10


    return price

def get_host_info(host_id):
    

    # list_ask = ['host_about', 'host_response_time', 'host_response_rate',
    #    'host_is_superhost', 'host_verifications', 
    #    'calculated_host_listings_count']

    hosts = pd.read_csv(os.getcwd() + "/repo/host_info.csv")
    host = hosts[hosts['host_id'] == host_id].reset_index()

    host_info = host.copy(deep=True)
    if host_info.shape[0] == 1:

        host_info['host_about'] = host_info['host_about'].apply(lambda x: 0 if pd.isnull(x) else 1)
        host_info['host_response_rate'] = host_info['host_response_rate'].str[:-1].astype('float64')

        host_info['host_response_rate'] = pd.cut(host_info['host_response_rate'],
                                           bins=[0, 50, 90, 99, 100],
                                           labels=['0-49%', '50-89%', '90-99%', '100%'],
                                           include_lowest=True)
        host_info['host_response_rate'] = host_info['host_response_rate'].astype('str')
        host_info['host_response_rate'] = host_info['host_response_rate'].replace('nan', 'unknown')
        host_info['host_response_time'] = host_info['host_response_time'].fillna("unknown")
        host_info['host_is_superhost'] = host_info['host_is_superhost'].map({'t': 1, 'f': 0})
        host_info['host_verifications'] = host_info['host_verifications'].apply(lambda row: len(row))
        host_info['host_has_profile_pic'] = host_info['host_has_profile_pic'].map({'t': 1, 'f': 0})
        host_info['host_identity_verified'] = host_info['host_identity_verified'].map({'t': 1, 'f': 0})
        host_info['calculated_host_listings_count'] = host_info['calculated_host_listings_count'].astype('float64').replace(0.0, 0.01)  # Replacing 0s with 0.01
        host_info['calculated_host_listings_count'] = np.log(host_info['calculated_host_listings_count'])

        host_info = host_info[['host_about', 'host_response_time', 'host_response_rate',
       'host_is_superhost', 'host_verifications', 'calculated_host_listings_count','host_identity_verified', 'host_has_profile_pic']]

        logger.error(host_info['host_about'])
        # logger.error(host_info['host_response_rate'])
        # logger.error(host_info['host_response_time'])
        # logger.error(host_info['host_is_superhost'])
        # logger.error(host_info['host_verifications'])
        # logger.error(host_info['host_has_profile_pic'])
        # logger.error(host_info['host_identity_verified'])
        return host_info
    elif host_info.shape[0] > 1:
        logger.error(f"Internal error, too many listings with same id")
        return {'error':'too many listings'}
    else:
        logger.error("No listing with id: {} exist".format(host_id))
        return None


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
    # pass
    # return info