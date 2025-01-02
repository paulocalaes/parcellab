'''
This file contains the WeatherDetail class which is a subclass of APIView.
This class is responsible for handling the GET request for the weather API.
'''
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .weather import WeatherService

# Configure logger
logger = logging.getLogger(__name__)

class WeatherDetail(APIView):
    """
    WeatherDetail class is a subclass of APIView.
    This class is responsible for handling the GET request for the weather API.
    """

    def get(self, request, zip_code, country_code, *args, **kwargs):
        """
        This method handles the GET request for the weather API.
        It takes in the zip code and country code as parameters and returns the weather data
        for the given zip code and country code.
        """
        logger.info("GET request received for weather data: zip_code=%s, country_code=%s",
                    zip_code, country_code)

        try:
            # Call the WeatherService to get weather data
            weather_service = WeatherService()
            response = weather_service.get_weather(zip_code, country_code)

            if response:
                logger.info("Successfully retrieved weather data for zip_code=%s, country_code=%s",
                            zip_code, country_code)
                return Response(response, status=status.HTTP_200_OK)
            logger.warning("Weather data not found for zip_code=%s, country_code=%s",
                               zip_code, country_code)
            return Response({"error": "Weather data not found"},
                                status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error("Error retrieving weather data for zip_code=%s, country_code=%s: %s",
                         zip_code, country_code, str(e))
            return Response({"error": "An error occurred while fetching the weather data"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
