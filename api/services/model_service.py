import os
from csv import reader, DictWriter
from unittest import result
# import requests
from base_logger import logger
from  geopy.distance import geodesic 
import pandas as pd
from flask import  abort, jsonify
import numpy as np

def main(data):
    """
    Orchestrates the transformation of the received data and uses the model to return the predicted price.

    :return:
    """
    # post shcema
    # data = {
#     "host_id":3159,
#     "latitude":52.36435,
#     "longitude":4.94358,
#     "room_type":"Private room",
#     "minimum_nights":3,
#     "maximum_nights":15
#     "accomodates": 2,
    # "neighbouhood": "ΓΚΥΖΙ",
    # "property_type": "Room in boutique hotel"  
    # "bathrooms": 1,
    # "shared":False,
    # "tv": True,
    # "kitchen":False,
    # "air_conditioning": True
#     }

    try:
        info = get_host_info(data['host_id'])

        # Error handling for the existance of the listing in our repo
        if not info:
            return None
        elif 'error' in info:
            return info
        
        preprocessed_data = preprocess_dataset(data)
        final_data= pd.concat([preprocessed_data, info], axis=1)
        price = get_price(final_data)

        price = np.exp(price)
        
        info_to_return = {
            "host_id": data['host_id'],
            "reviews_per_month": info['reviews_per_month'],
            "neighbourhood": data['neighbourhood'],
            "room_type": data['room_type']

        }

        return {'listing_info': info_to_return, 'prediction': {'price': price}}
    
    except Exception as exception:
        logger.error(f"Could not predict price {exception}")
        return None

def preprocess_dataset(data):
    # some of the below we ask 
    feature_names = ['neighbourhood_cleansed',
       'latitude', 'longitude', 'property_type', 'room_type', 'accommodates',
       'minimum_nights', 'maximum_nights', 'has_availability',
       'availability_30', 'availability_365', 'number_of_reviews', 'license',
       'instant_bookable', 'kitchen', 'air_conditioning', 'balcony',
       'bed_linen', 'tv', 'coffee_machine', 'cooking_basics', 'elevator',
       'parking', 'outdoor_space', 'host_greeting', 'internet',
       'long_term_stays', 'private_entrance', 'neighbourhood',
       'amenities_number', 'distance_center', 'shared_bath', 'bathrooms',
       'occupancy', 'bookings_per_year']


    # features = pd.DataFrame(columns = feature_names)
    try:
        data = pd.DataFrame(data, index=[0])
        
        data = log_transform(data)
        distance = get_distance(data[['latitude', 'longitude']])
        neigh = get_neigh_group(data[['neighbourhood']])
        prop_type = pd.get_dummies(data[['property_type']])
        room_type = pd.get_dummies(data[['room_type']])
        data.drop(columns=['neighbourhood', 'property_type','room_type'], inplace=True)

        data = pd.concat([data, distance, neigh, prop_type, room_type], axis=1)
        # logger.error(data)
        # Add more
        return data
    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")


def log_transform(df):
    numerical_columns = ['neighborhood_overview',
        'host_listings_count', 'host_verifications', 'accommodates',
       'bedrooms', 'beds', 'minimum_nights', 'maximum_nights', 'number_of_reviews',
       'number_of_reviews_ltm', 'number_of_reviews_l30d', 
       'calculated_host_listings_count',
       'reviews_per_month', 'amenities_number',
        'bathrooms', 'occupancy',
       'bookings_per_year', 'price']

    for col in numerical_columns:
        try:
            df[col] = df[col].astype('float64').replace(0.0, 0.01) # Replacing 0s with 0.01
            df[col] = np.log(df[col])
        except:
            continue
    return df

def get_neigh_group(data_neighbourhood):
    neigh_group = pd.read_csv(...)
    data_neighbourhood['neighbourhood_cleansed_group'] = data_neighbourhood['neighbourhood_cleansed'].map(neigh_group)
    data_neighbourhood = pd.get_dummies(data_neighbourhood)
    data_neighbourhood.drop(columns=['neighbourhood_cleansed_group'], inplace=True)
    return data_neighbourhood

def get_distance(data):
    data['lat_center'] = 37.9715
    data['lon_center'] = 23.7257
    data['distance_center'] = data.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    data = data.drop(columns = ['lat_center', 'lon_center'])
    return data

def get_price(data):
    # TODO
    # model = model.load("xxx")
    # scaler = scaler.laod()
    # data_scaled = scaler.transform()
    # price = model.predict(data_scaled)
    price = 50
    
    return price

def get_host_info(host_id):
    

    # info_to_get = ['host_about', 'host_response_time', 'host_response_rate',
    #    'host_is_superhost', 'host_verifications',  'number_of_reviews', 'license',
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
        