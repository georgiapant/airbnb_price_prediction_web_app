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

    :return: the data to be presented  (host information and predicted price)
    """
    try:
        final_data = preprocess_dataset(data)
        price = get_price(final_data)
        info_to_return = {
            "host_id": int(data['host_id']),
            "number_of_reviews": int(final_data['number_of_reviews'].iloc[0]),
            "neighbourhood_cleansed": data['neighbourhood_cleansed'],
            "room_type": data['room_type'],
            "price": round(float(price),2)
        }
        # return {'listing_info': info_to_return, 'prediction': {'price': int(price)}}
        return {'price': round(float(price),2)}
        # return {'info': info_to_return}
        
    
    except Exception as exception:
        logger.error(f"Could not predict price {exception}")
        return None


def preprocess_dataset(data):
    """
    Function for the preprocessing of the input data. This includes preprocessing of the linsting info, amenities
    and host info. 

    :return: preprocessed data
    """

    try:
        df = pd.DataFrame.from_dict({"data": data}, orient="index")
        df.reset_index(inplace=True, drop=True)
        host_info = host_info_proc(data['host_id'])
        amenities = amenities_proc(df['amenities'])
        listing_info = listing_info_proc(df)
        final_data = pd.concat([host_info, listing_info, amenities], axis=1,ignore_index=False)
        return final_data

    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")


def host_info_proc(host_id):
    """
    Function that preprocess the information related to the desired host. Based on the given host id and a csv file including information
    about all hosts.

    :return: preprocessed data related to host
    """    
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
        return host_info
    elif host_info.shape[0] > 1:
        logger.error(f"Internal error, too many listings with same id")
        return {'error':'too many listings'}
    else:
        logger.error("No listing with id: {} exist".format(host_id))
        return None

def amenities_proc(amenities):
    """
    Function for the preprocessing of the amenities. The preprocessing includes the creation of a dataframe, where
    each column represent each amenity with an indication of whether exists or not. Also returns column with the 
    total number of amenites that exist

    :return: preprocessed amenities data
    """
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
        'hot_tub_sauna_or_pool': (1 if 'hot_tub_sauna_or_pool' in amenities else 0),
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

def listing_info_proc(data):
    """
    Function for the preprocessing of the listing info. Also this function includes the implementation of some new features

    :return: preprocessed listing info with new features
    """
    with open(os.getcwd() + "/repo/neighbourhood_groupings.json", "r", encoding="utf8") as read_content:
        neigh_group = json.load(read_content)
    # process exesting listing info
    data['latitude'] = float(data['latitude'])
    data['longitude'] = float(data['longitude'])
    data['maximum_nights'] = int(data['maximum_nights'])
    data['minimum_nights'] = int(data['minimum_nights'])
    data['accommodates'] = int(data['accommodates'])
    data['number_of_reviews'] = int(data['number_of_reviews'])
    data['availability_90'] = int(data['availability_90'])
    data['shared_bath'] = data['shared_bath'].astype(int)
    data['has_availability'] = data['has_availability'].astype(int)
    data['license'] = data['license'].astype(int)
    data['instant_bookable'] = data['instant_bookable'].astype(int)
    #Create new features
    data['lat_center'] = 37.9715
    data['lon_center'] = 23.7257
    data['neighbourhood_cleansed_group'] = data['neighbourhood_cleansed'].map(neigh_group)
    data['distance_parthenon'] = data.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    # Delete unnecessary data
    data = data.drop(columns=['lat_center','lon_center','amenities','host_id'])
    return data

def get_price(data):
    """
    Function that predicts the price based on the implemented model

    :return: the predicted price
    """
    loaded_model = joblib.load(os.getcwd() + "/repo/pipeline.pkl")
    price = loaded_model.predict(data)
    return price

