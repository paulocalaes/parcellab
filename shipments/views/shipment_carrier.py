'''
This module contains the ShipmentCarrier class which handles GET requests
for retrieving shipments based on the carrier
'''
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from weather.weather import WeatherService

# Configure the logger
logger = logging.getLogger(__name__)

class ShipmentCarrier(APIView):
    """
    This class handles GET requests for retrieving shipments based on the carrier
    and appending weather data to each shipment's information.
    """

    def get(self, request, carrier, *args, **kwargs):
        """
        Handle GET requests to retrieve shipments for a specific carrier.
        For each shipment, weather data is fetched and appended to the shipment information.

        Args:
            request: The incoming HTTP request.
            carrier: The carrier for which shipments need to be fetched.

        Returns:
            Response: A Response object containing shipment data with weather information.
        """
        logger.info("GET request received for shipments with carrier: %s", carrier)

        try:
            # Retrieve the shipment objects based on carrier
            shipments = Shipment.objects.filter(carrier=carrier)

            if not shipments.exists():
                logger.warning("No shipments found for carrier: %s", carrier)
                return Response({"error": "No shipments found for the specified carrier"},
                                status=status.HTTP_404_NOT_FOUND)

            shipment_data_list = []

            # Iterate over each shipment and fetch the weather data
            for shipment in shipments:
                weather = WeatherService().get_weather(
                    shipment.receiver_zip_code, shipment.receiver_country_code)

                # Serialize the shipment data and append weather info
                shipment_data = ShipmentSerializer(shipment).data
                shipment_data['weather'] = weather

                shipment_data_list.append(shipment_data)

            logger.info("Successfully retrieved shipments for carrier: %s", carrier)
            return Response({'data': shipment_data_list}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error processing shipments for carrier: %s: %s", carrier, str(e))
            return Response({"error": "An error occurred while retrieving the shipments"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
