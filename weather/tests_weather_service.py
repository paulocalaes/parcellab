from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase
from weather.weather import WeatherService
from weather.weather import requests
from weather.models import Weather
from datetime import datetime



class WeatherServiceTests(APITestCase):
    """
    Test suite for the WeatherService class.
    """

    @patch('redis.Redis.get')
    def test_get_weather_redis_success(self, mock_redis):
        """
        Test getting weather data from Redis cache.
        """
        # Mock the Redis connection and the cached weather data
        mock_redis.return_value = b"72.5,Sunny"

        weather_service = WeatherService()

        result = weather_service.get_weather_redis('94103', 'US')

        # Assert that the weather data is returned and source is 'Redis'
        self.assertEqual(result['temperature'], '72.5')
        self.assertEqual(result['condition'], 'Sunny')
        self.assertEqual(result['source'], 'Redis')

    @patch('redis.Redis.get')
    def test_get_weather_redis_not_found(self, mock_redis):
        """
        Test when no weather data is found in Redis.
        """
        mock_redis.return_value = None  # Simulate no cached data

        weather_service = WeatherService()
        result = weather_service.get_weather_redis('94103', 'US')

        self.assertIsNone(result)

    @patch('weather.weather.Weather.objects.filter')
    def test_get_weather_db_success(self, mock_filter):
        """
        Test getting weather data from the database.
        """
        # Mock the Weather object returned by the database query
        # Use spec=Weather to ensure the mock behaves like the Weather model
        mock_weather = Weather()
        mock_weather.zip_code = "94103"
        mock_weather.country_code = "US"
        mock_weather.temperature = 72.5
        mock_weather.condition = "Sunny"
        mock_weather.last_fetched = datetime.now()

        mock_filter.return_value.first.return_value = mock_weather
        
        # Create an instance of WeatherService and call get_weather_db
        weather_service = WeatherService()
        result = weather_service.get_weather_db('94103', 'US')
        
        # Assertions to check that the returned result matches the mock weather data
        self.assertEqual(result['temperature'], 72.5)
        self.assertEqual(result['condition'], 'Sunny')
        self.assertEqual(result['source'], 'Database')

    @patch('weather.weather.Weather.objects.filter')
    def test_get_weather_db_not_found(self, mock_filter):
        """
        Test when no weather data is found in the database.
        """
        mock_filter.return_value.first.return_value = None  # Simulate no weather data

        weather_service = WeatherService()
        result = weather_service.get_weather_db('94103', 'US')

        self.assertIsNone(result)

    @patch('weather.weather.requests.get')
    def test_get_weather_api_success(self, mock_get):
        """
        Test getting weather data from the OpenWeatherMap API.
        """
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 72.5},
            'weather': [{'description': 'Sunny'}]
        }
        mock_get.return_value = mock_response

        weather_service = WeatherService()
        result = weather_service.get_weather_api('94103', 'US')

        self.assertEqual(result['temperature'], 72.5)
        self.assertEqual(result['condition'], 'Sunny')
        self.assertEqual(result['source'], 'API')

    @patch('weather.weather.requests.get')
    def test_get_weather_api_failure(self, mock_get):
        """
        Test when the OpenWeatherMap API request fails.
        """
        # Mock the API to return a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        weather_service = WeatherService()
        result = weather_service.get_weather_api('94103', 'US')

        self.assertIsNone(result)

    @patch('weather.weather.requests.get')
    def test_get_weather_api_exception(self, mock_get):
        """
        Test when there is an exception (e.g., network issue) while fetching from the OpenWeatherMap API.
        """
        # Mock the request to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        weather_service = WeatherService()
        result = weather_service.get_weather_api('94103', 'US')

        self.assertIsNone(result)

    @patch('weather.weather.WeatherService.get_weather_redis')
    @patch('weather.weather.WeatherService.get_weather_db')
    @patch('weather.weather.WeatherService.get_weather_api')
    def test_get_weather_success_redis(self, mock_api, mock_db, mock_redis):
        """
        Test the full get_weather method with Redis as the source.
        """
        mock_redis.return_value = {'temperature': '72.5', 'condition': 'Sunny', 'source': 'Redis'}
        result = WeatherService().get_weather('94103', 'US')

        self.assertEqual(result['source'], 'Redis')

    @patch('weather.weather.WeatherService.get_weather_redis')
    @patch('weather.weather.WeatherService.get_weather_db')
    @patch('weather.weather.WeatherService.get_weather_api')
    def test_get_weather_success_db(self, mock_api, mock_db, mock_redis):
        """
        Test the full get_weather method with Database as the source when Redis does not return data.
        """
        mock_redis.return_value = None
        mock_db.return_value = {'temperature': '72.5', 'condition': 'Sunny', 'source': 'Database'}
        result = WeatherService().get_weather('94103', 'US')

        self.assertEqual(result['source'], 'Database')

    @patch('weather.weather.WeatherService.get_weather_redis')
    @patch('weather.weather.WeatherService.get_weather_db')
    @patch('weather.weather.WeatherService.get_weather_api')
    def test_get_weather_success_api(self, mock_api, mock_db, mock_redis):
        """
        Test the full get_weather method with OpenWeatherMap API as the source when Redis and DB return no data.
        """
        mock_redis.return_value = None
        mock_db.return_value = None
        mock_api.return_value = {'temperature': 72.5, 'condition': 'Sunny', 'source': 'API'}

        result = WeatherService().get_weather('94103', 'US')

        self.assertEqual(result['source'], 'API')

    def test_get_weather_no_data(self):
        """
        Test the full get_weather method when no data is found in any source.
        """
        with patch('weather.weather.WeatherService.get_weather_redis', return_value=None), \
             patch('weather.weather.WeatherService.get_weather_db', return_value=None), \
             patch('weather.weather.WeatherService.get_weather_api', return_value=None):
            result = WeatherService().get_weather('94103', 'US')

        self.assertIsNone(result)
