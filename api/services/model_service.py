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
    #resultset = [value for key, value in your_dict.items() if key not in your_blacklisted_set]
    # logger.error(f"Could not predict price {data}")
    try:


        final_data = preprocess_dataset(data)
        price = get_price(final_data)

        info_to_return = {
            "host_id": int(data['host_id']),
            "number_of_reviews": int(final_data['number_of_reviews'].iloc[0]),
            "neighbourhood_cleansed": data['neighbourhood_cleansed'],
            "room_type": data['room_type']
        }

        # return {'listing_info': info_to_return, 'prediction': {'price': int(price)}}
        return {'price': int(price)}
        
    
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
        df = pd.DataFrame.from_dict({"data": data}, orient="index")
        df.reset_index(inplace=True, drop=True)

        amenities = get_amenities(df['amenities'])

        listing_info = missing_values_n_encoding(df)

        host_info = get_host_info(data['host_id'])
        final_data = pd.concat([host_info, listing_info, amenities], axis=1,ignore_index=False)
        # final_data = pd.concat([listing_info], axis=1,ignore_index=False)

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

        # final_data.to_csv(os.getcwd() +'/test.csv')
        return final_data
    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")

def get_amenities(amenities):
    amenities_data = pd.DataFrame(data = {
        'kitchen': (1 if 'kitchen' in amenities else 0),
        'air_conditioning': (1 if 'air_conditioning' in amenities else 0),
        'high_end_electronics': (1 if 'high_end_electronics' in amenities else 0),
        'bbq': (1 if 'bbq' in amenities else 0),
        'balcony': (1 if 'balcony' in amenities else 0),
        'nature_and_views': (1 if 'nature_and_views' in amenities else 0),
        'bed_linen': (1 if 'bed_linen' in amenities else 0),
        'breakfast': (1 if 'breakfast' in amenities else 0),
        'tv': (1 if 'tv' in amenities else 0),
        'coffee_machine': (1 if 'coffee_machine' in amenities else 0),
        'cooking_basics': (1 if 'cooking_basics' in amenities else 0),
        'elevator': (1 if 'elevator' in amenities else 0),
        'gym': (1 if 'gym' in amenities else 0),
        'child_friendly': (1 if 'child_friendly' in amenities else 0),
        'parking': (1 if 'parking' in amenities else 0),
        'outdoor_space': (1 if 'outdoor_space' in amenities else 0),
        'host_greeting': (1 if 'host_greeting' in amenities else 0),
        'hot_tub_sauna_or_pool': (1 if 'host_greeting' in amenities else 0),
        'internet': (1 if 'internet' in amenities else 0),
        'long_term_stays': (1 if 'long_term_stays' in amenities else 0),
        'pets_allowed': (1 if 'pets_allowed' in amenities else 0),
        'private_entrance': (1 if 'private_entrance' in amenities else 0),
        'secure': (1 if 'secure' in amenities else 0),
        'self_check_in': (1 if 'self_check_in' in amenities else 0),
        'smoking_allowed': (1 if 'smoking_allowed' in amenities else 0),
        'accessible': (1 if 'accessible' in amenities else 0),
        'event_suitable': (1 if 'event_suitable' in amenities else 0)
}, index=[0])

    amenities_data = amenities_data.astype(int)
    amenities_data["amenities_number"] = amenities_data.sum(axis=1)
    logger.error(amenities_data)
    return amenities_data

    # amenities = pd.DataFrame.from_dict({"amen": amenities_data}, orient='index')
    # amenities.reset_index(inplace=True, drop=True)
    # amenities = amenities.astype(int)
    # amenities["amenities_number"] = amenities.sum(axis=1)
    # logger.error(amenities)
    # return amenities



def missing_values_n_encoding(data):

    #     'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type',
    #     'room_type', 'accommodates','minimum_nights', 'maximum_nights',
    #     'availability_90', 'number_of_reviews', 'bathrooms']

    # logger.error(listing_info)

    data['latitude'] = int(data['latitude'])
    data['longitude'] = int(data['longitude'])
    data['maximum_nights'] = int(data['maximum_nights'])
    data['minimum_nights'] = int(data['minimum_nights'])
    data['accommodates'] = int(data['accommodates'])
    data['number_of_reviews'] = int(data['number_of_reviews'])
    data['availability_90'] = int(data['availability_90'])

    
    with open(os.getcwd() + "/repo/neighbourhood_groupings.json", "r", encoding="utf8") as read_content:
        neigh_group = json.load(read_content)

    # listing_data = pd.DataFrame.from_dict({"info": listing_data}, orient='index')
    # , orient = 'index'
    # listing_data.reset_index(inplace=True, drop=True)


    data['lat_center'] = 37.9715
    data['lon_center'] = 23.7257

    logger.error(type(data['neighbourhood_cleansed']))

    data['neighbourhood_cleansed_group'] = data['neighbourhood_cleansed'].map(neigh_group)
    data['distance_parthenon'] = data.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    data = data.drop(columns=['lat_center','lon_center','amenities','host_id'])

    data['shared_bath'] = data['shared_bath'].astype(int)
    data['has_availability'] = data['has_availability'].astype(int)
    data['license'] = data['license'].astype(int)
    data['instant_bookable'] = data['instant_bookable'].astype(int)

    return data


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
    host = hosts[hosts['host_id'] == int(host_id)].reset_index()

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

        # logger.error(host_info['host_about'])
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