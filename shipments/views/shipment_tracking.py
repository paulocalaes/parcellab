'''
This module contains the ShipmentTracking class which handles tracking shipments
based on tracking number.
'''
import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from weather.weather import WeatherService

# Configure logger
logger = logging.getLogger(__name__)


class ShipmentTracking(APIView):
    """
    This class handles tracking shipments based on tracking number.
    It retrieves shipment data and associated weather information.
    """

    def get(self, request, tracking_number, *args, **kwargs):
        """
        Handle GET requests to retrieve shipment data along with weather
        information for a given tracking number.

        Args:
            request: The incoming HTTP GET request.
            tracking_number: The tracking number of the shipment.

        Returns:
            Response: A Response object containing shipment and weather data or an error message.
        """
        logger.info("GET request received for tracking number: %s",
                    tracking_number)

        try:
            # Retrieve the shipment object based on tracking_number
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            logger.info("Shipment found for tracking number: %s",
                        tracking_number)

            # Fetch weather data for the shipment's destination
            weather = WeatherService().get_weather(
                shipment.receiver_zip_code, shipment.receiver_country_code)
            logger.info(
                "Weather data retrieved for shipment with tracking number: %s", tracking_number)

            # Serialize the shipment data
            shipment_data = ShipmentSerializer(shipment).data

            # Return response with shipment and weather data
            return Response({'shipment': shipment_data, 'weather': weather},
                            status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.warning(
                "Shipment not found for tracking number: %s", tracking_number)
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                "Error processing shipment with tracking number %s: %s", tracking_number, str(e))
            return Response({"error": "An error occurred while processing the shipment"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
