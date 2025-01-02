'''
This module contains the views for the Shipment app.
'''
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer

# Configure the logger
logger = logging.getLogger(__name__)

class ShipmentList(APIView):
    """
    This class handles listing all shipments and creating a new shipment.
    It supports GET and POST requests.
    """

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests to list all shipments.
        
        Args:
            request: The incoming HTTP GET request.

        Returns:
            Response: A Response object containing the list of shipments.
        """
        logger.info("GET request received to list all shipments.")

        try:
            shipments = Shipment.objects.all()
            serializer = ShipmentSerializer(shipments, many=True)
            logger.info("Successfully retrieved all shipments.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving shipments: %s", str(e))
            return Response({"error": "An error occurred while retrieving shipments"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ShipmentSerializer)
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests to create a new shipment.

        Args:
            request: The incoming HTTP POST request containing the shipment data.

        Returns:
            Response: A Response object containing the created shipment data or errors.
        """
        logger.info("POST request received to create a new shipment.")

        try:
            serializer = ShipmentSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()  # This will also create related articles
                logger.info("Successfully created new shipment.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning("Failed to create shipment: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error creating shipment: %s", str(e))
            return Response({"error": "An error occurred while creating the shipment"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
