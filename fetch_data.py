import pandas as pd
import requests
import datetime as dt
import json
import meteomatics.api as api

def get_data():

    with open("config.json") as f:
        data = json.load(f)

    username = data['User']
    password = data['Password']

    parameters = ['t_2m:C']
    model = 'mix'
    startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    enddate = startdate + dt.timedelta(days=7)
    interval = dt.timedelta(hours=1)

    locations = {
        "Athens, Greece": (+37.9755648, 23.7348324),
        "London, UK": (51.5073219, -0.1276474),
        "Berlin, Germany": (+52.5170365, 13.3888599)
    }

    data_dict = {}

    for location, coordinates in locations.items():
        response = api.query_time_series([coordinates], startdate, enddate, interval, parameters, username, password, model=model)
        response.reset_index(inplace=True)
        response.drop(columns=['lat', 'lon'], inplace=True)
        response.rename(columns={'validdate': 'time', 't_2m:C': 'temperature_c'}, inplace=True)
        data_dict[location] = response.to_dict(orient='records')

    if data_dict is not None:
        print('LOG: data downloaded from api')

    return data_dict
