'''
This file contains the WeatherService class which is responsible for fetching 
weather data from Redis, Database or OpenWeatherMap API.
The get_weather method is used to get the weather data from the above sources.
'''
import logging
from datetime import datetime, timedelta
from django.conf import settings
import requests
import redis
from .models import Weather
from .serializers import WeatherSerializer

# Configure logger
logger = logging.getLogger(__name__)

API_URL = 'http://api.openweathermap.org/data/2.5/'


class WeatherService:
    '''
    WeatherService class is responsible for fetching weather data from Redis, 
    Database or OpenWeatherMap API.
    '''

    # Redis connection
    r = redis.Redis(host='redis', port=6379, db=0)

    def get_weather_redis(self, zip_code, country_code):
        '''
        Fetch weather data from Redis cache
        '''
        logger.info("Attempting to fetch weather from Redis for zip_code=%s, country_code=%s",
                    zip_code, country_code)

        try:
            cached_weather = self.r.get(f'weather:{zip_code}, {country_code}')
            if cached_weather:
                temperature, condition = cached_weather.decode(
                    'utf-8').split(',')
                logger.info(
                    "Successfully retrieved weather from Redis for zip_code=%s, country_code=%s",
                    zip_code, country_code)
                return {'temperature': temperature, 'condition': condition, 'source': 'Redis'}
            logger.info(
                "No weather data found in Redis for zip_code=%s, country_code=%s",
                zip_code, country_code)
        except Exception as e:
            logger.error("Error retrieving weather from Redis for zip_code=%s, country_code=%s: %s",
                         zip_code, country_code, str(e))
        return None

    def get_weather_db(self, zip_code, country_code):
        '''
        Fetch weather data from Database
        '''
        logger.info(
            "Attempting to fetch weather from Database for zip_code=%s, country_code=%s",
            zip_code, country_code)

        try:
            weather = Weather.objects.filter(
                zip_code=zip_code, country_code=country_code).first()
            # If weather data is available and fetched under 2 hours, return it
            if weather and weather.last_fetched > datetime.now() - timedelta(hours=2):
                
                # Cache the data in Redis for 2 hours
                self.r.setex(f'weather:{zip_code}, {country_code}',
                             7200, f"{weather.temperature},{weather.condition}")
                serializer = WeatherSerializer(weather)
                serialized_data = serializer.data
                serialized_data['source'] = 'Database'
                logger.info(
                    "Successfully retrieved weather from Database for zip_code=%s, country_code=%s",
                    zip_code, country_code)
                return serialized_data
            logger.info(
                "No fresh weather data found in Database for zip_code=%s, country_code=%s",
                zip_code, country_code)
        except Exception as e:
            logger.error("Error retrieving weather from Database for zip_code=%s, country_code=%s: %s",
                         zip_code, country_code, str(e))
        return None

    def get_weather_api(self, zip_code, country_code):
        '''
        Fetch weather data from OpenWeatherMap API
        '''
        logger.info(
            "Attempting to fetch weather from OpenWeatherMap API for zip_code=%s, country_code=%s",
            zip_code, country_code)

        try:
            # Fetch weather from OpenWeatherMap API if not cached
            api_key = settings.OPENWEATHER_API_KEY
            url = f"{API_URL}weather?zip={zip_code},{country_code}&appid={api_key}&units=imperial"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                condition = data['weather'][0]['description']

                # Cache the data in Redis for 2 hours
                self.r.setex(
                    f'weather:{zip_code}, {country_code}', 7200, f"{temperature},{condition}")

                # Save the weather data to the database
                Weather.objects.update_or_create(
                    zip_code=zip_code,
                    defaults={'temperature': temperature,
                              'condition': condition, 'last_fetched': datetime.now()}
                )

                logger.info(
                    "Successfully fetched weather from OpenWeatherMap API for zip_code=%s, country_code=%s",
                    zip_code, country_code)
                return {'temperature': temperature, 'condition': condition, 'source': 'API'}
            logger.warning(
                "Failed to fetch weather data from OpenWeatherMap API for zip_code=%s, country_code=%s: %s",
                zip_code, country_code, response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error(
                "Error making request to OpenWeatherMap API for zip_code=%s, country_code=%s: %s",
                zip_code, country_code, str(e))
        return None

    def get_weather(self, zip_code, country_code):
        '''
        Get the weather data from Redis, Database or OpenWeatherMap API
        '''
        logger.info(
            "Attempting to get weather data for zip_code=%s, country_code=%s",
            zip_code, country_code)

        # Check Redis, then Database, and finally the OpenWeatherMap API
        weather = self.get_weather_redis(zip_code, country_code)
        if weather:
            return weather

        weather = self.get_weather_db(zip_code, country_code)
        if weather:
            return weather

        weather = self.get_weather_api(zip_code, country_code)
        if weather:
            return weather
        
        logger.error(
            "Unable to fetch weather data for zip_code=%s, country_code=%s", zip_code, country_code)
        return None
