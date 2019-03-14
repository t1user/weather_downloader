import requests
import json
import time
import pickle
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from key import key
from db_schema import Weather, Base, Forecast, Item


def download_data(url, params, retries=10):
    for _ in range(retries):
        try:
            result = requests.get(url, params)
            result.raise_for_status()
            return json.loads(result.text)
        except:
            time.sleep(15)


def do_weather(ids):
    ids_str = ','.join(ids)
    # download current weather data
    current_url = 'http://api.openweathermap.org/data/2.5/group'
    current_params = {
        'id': ids_str,
        'units': 'metric',
        'APPID': key
    }
    current = download_data(current_url, current_params)

    # save current weather to the database
    for item in current['list']:
        data = Weather(
            city=item['name'],
            temperature=item['main']['temp'],
            pressure=item['main']['pressure'],
            humidity=item['main']['humidity'],
            temp_min=item['main']['temp_min'],
            temp_max=item['main']['temp_max'],
            weather=item['weather'][0]['main'],
            weather_detail=item['weather'][0]['description'],
            visibility=item.get('visibility'),
            wind_speed=item['wind'].get('speed'),
            wind_deg=item['wind'].get('deg'),
            wind_gust=item['wind'].get('gust'),
            clouds=item['clouds']['all'],
            dt=datetime.datetime.utcfromtimestamp(item['dt'])
        )
        session.add(data)
    session.commit()


def do_forecasts(id):
    # download forecasts
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    forecast_params = {
        'id': id,
        'units': 'metric',
        'APPID': key
    }
    forecast = download_data(forecast_url, forecast_params)

    # save forecasts to the database
    forecast_for_db = Forecast(
        city=forecast['city']['name'],
    )
    session.add(forecast_for_db)
    session.commit()
    counter = 0
    for f in forecast['list']:
        data = Item(
            t=counter,
            temperature=f['main']['temp'],
            temp_min=f['main']['temp_min'],
            temp_max=f['main']['temp_max'],
            pressure=f['main']['pressure'],
            humidity=f['main']['humidity'],
            weather=f['weather'][0]['main'],
            weather_detail=f['weather'][0]['description'],
            clouds=f['clouds']['all'],
            wind_speed=f['wind'].get('speed'),
            wind_deg=f['wind'].get('deg'),
            wind_gust=f['wind'].get('gust'),
            rain=f.get('rain', {'3h': None}).get('3h'),
            dt=datetime.datetime.utcfromtimestamp(f['dt']),
            forecast_id=forecast_for_db.id,
        )
        session.add(data)
        counter += 1
    session.commit()


if __name__ == '__main__':
    # create database session
    engine = create_engine('sqlite:///data.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # download ids of locations
    with open('id_dict.pickle', 'rb') as f:
        ids_dict = pickle.load(f)
    ids = [str(i) for city, i in ids_dict.items()]

    do_weather(ids)

    for id in ids:
        do_forecasts(id)
