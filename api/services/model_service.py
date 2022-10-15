import os
from csv import reader, DictWriter
from unittest import result
# import requests
from base_logger import logger
from  geopy.distance import geodesic 
import pandas as pd
from flask import  abort, jsonify

def main(data):
    """
    Orchestrates the transformation of the received data and uses the model to return the predicted price.

    :return:
    """
    # post shcema
    # data = {
#     "id":52959885,
#     "host_id":3159,
#     "latitude":52.36435,
#     "longitude":4.94358,
#     "room_type":"Private room",
#     "minimum_nights":3,
#     "accomodates": 2,
#     "beds": 1,
#     "has_wifi": 1,
#     }

    try:
        info = get_info(data['id'])

        # Error handling for the existance of the listing in our repo
        if not info:
            return None
        elif 'error' in info:
            return info
        
        preprocessed_data = preprocess_dataset(data)
        price = get_price(preprocessed_data)
        return {'listing_info': info, 'prediction': {'price': price}}
    
    except Exception as exception:
        logger.error(f"Could not predict price {exception}")
        return None

def preprocess_dataset(data):
    try:
        data = pd.DataFrame(data, index=[0])
        data['room_type'] = data['room_type'].map({'Shared room': 1, 'Private room': 2, 'Hotel room':3, 'Entire home/apt': 4})
        data = get_distance(data)
        # logger.error(data)
        # Add more
        return data
    except Exception as exception:
        logger.error(f"Could not preprocess data, exception: {exception}")

def get_distance(data):
    data['lat_center'] = 37.983810
    data['lon_center'] = 23.727539
    data['distance_center'] = data.apply(lambda x: geodesic((x['latitude'], x['longitude']), (x['lat_center'], x['lon_center'])).km, axis = 1)
    data = data.drop(columns = ['lat_center', 'lon_center', 'latitude', 'longitude'])
    return data

def get_price(data):
    # TODO
    # model = model.load("xxx")
    # scaler = scaler.laod()
    # data_scaled = scaler.transform()
    # price = model.predict(data_scaled)
    price = 50
    
    return price

def get_info(listing_id):
    
    info_all = pd.read_csv(os.getcwd() + "/api/repo/listings_info.csv")
    info = {}
    info_id = info_all[info_all['id'] == listing_id]
    if info_id.shape[0] == 1:
        info['neighbourhood'] = info_id['neighbourhood_cleansed'].item()
        info['reviews_per_month'] = info_id['reviews_per_month'].item()
        info['room_type'] = info_id['room_type'].item()
        return info
    elif info_id.shape[0] > 1:
        logger.error(f"Internal error, too many listings with same id")
        return {'error':'too many listings'}
    else:
        logger.error("No listing with id: {} exist".format(listing_id))
        return None
        # abort(400)
        