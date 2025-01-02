from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from weather.views import WeatherDetail
from django.urls import reverse


class WeatherDetailTests(APITestCase):
    """
    Test suite for the WeatherDetail view.
    """

    def setUp(self):
        """
        Set up test data and prepare the API endpoint for testing.
        """
        self.url = reverse('weather-detail', kwargs={'version': 'v1', 'country_code': 'US', 'zip_code': '94103'})

    @patch('weather.views.WeatherService')  # Mock the WeatherService
    def test_get_weather_success(self, MockWeatherService):
        """
        Test GET request to successfully retrieve weather data for a valid zip code and country.
        """

        # Mock the response from the WeatherService
        mock_weather_data = {
            'temperature': 72.5,
            'condition': 'Sunny',
            'source': 'API'
        }

        mock_service = MockWeatherService.return_value
        mock_service.get_weather.return_value = mock_weather_data

        # Make the GET request
        response = self.client.get(self.url)

        # Assert the status code and the returned data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature'], 72.5)
        self.assertEqual(response.data['condition'], 'Sunny')

    @patch('weather.views.WeatherService')  # Mock the WeatherService
    def test_get_weather_not_found(self, MockWeatherService):
        """
        Test GET request when no weather data is found for the given zip code and country.
        """

        # Mock the response from the WeatherService as {"error": "Weather data not found"} and return code 404
        mock_service = MockWeatherService.return_value
        mock_service.get_weather.return_value = None 
        

        # Make the GET request
        response = self.client.get(self.url)

        # Assert the status code and error message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Weather data not found')

    @patch('weather.views.WeatherService')  # Mock the WeatherService
    def test_get_weather_service_error(self, MockWeatherService):
        """
        Test GET request when an error occurs in the WeatherService.
        """

        # Mock the service to raise an exception
        mock_service = MockWeatherService.return_value
        mock_service.get_weather.side_effect = Exception("Error fetching weather")

        # Make the GET request
        response = self.client.get(self.url)

        # Assert the status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'An error occurred while fetching the weather data')

    def test_get_weather_invalid_zip_code(self):
        """
        Test GET request for an invalid zip code.
        This could happen if the view doesn't handle validation properly.
        """
        invalid_url = reverse('weather-detail', kwargs={'version': 'v1', 'country_code': 'US', 'zip_code': 'invalid_zip'})
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
