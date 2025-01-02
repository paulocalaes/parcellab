'''
This module contains the views for the Shipment app.
'''
import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer

# Configure logger
logger = logging.getLogger(__name__)

class ShipmentDetail(APIView):
    """
    This class handles retrieving, updating, partially updating, and deleting shipments.
    """

    def get(self, request, shipment_id, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve a specific shipment by its ID.
        If no shipment_id is provided, it will list all shipments.

        Args:
            request: The incoming HTTP request.
            shipment_id: The ID of the shipment to retrieve.

        Returns:
            Response: A Response object containing shipment data or an error message.
        """
        logger.info("GET request received for shipment ID: %s", shipment_id)

        try:
            shipment = Shipment.objects.get(id=shipment_id)
            serializer = ShipmentSerializer(shipment)
            logger.info("Successfully retrieved shipment ID: %s", shipment_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.warning("Shipment with ID %s not found", shipment_id)
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ShipmentSerializer)
    def put(self, request, shipment_id, *args, **kwargs) -> Response:
        """
        Handle PUT requests to update an existing shipment completely.

        Args:
            request: The incoming HTTP request with updated data.
            shipment_id: The ID of the shipment to update.

        Returns:
            Response: A Response object containing updated shipment data or errors.
        """
        logger.info("PUT request received for updating shipment ID: %s", shipment_id)

        try:
            shipment = Shipment.objects.get(id=shipment_id)
        except ObjectDoesNotExist:
            logger.warning("Shipment with ID %s not found for update", shipment_id)
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShipmentSerializer(shipment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            logger.info("Successfully updated shipment ID: %s", shipment_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Failed to update shipment ID %s: %s", shipment_id, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ShipmentSerializer)
    def patch(self, request, shipment_id, *args, **kwargs) -> Response:
        """
        Handle PATCH requests to partially update an existing shipment.

        Args:
            request: The incoming HTTP request with partial update data.
            shipment_id: The ID of the shipment to partially update.

        Returns:
            Response: A Response object containing updated shipment data or errors.
        """
        logger.info("PATCH request received for updating shipment ID: %s", shipment_id)

        try:
            shipment = Shipment.objects.get(id=shipment_id)
        except ObjectDoesNotExist:
            logger.warning("Shipment with ID %s not found for partial update", shipment_id)
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShipmentSerializer(shipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Successfully partially updated shipment ID: %s", shipment_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Failed to partially update shipment ID %s: %s", 
                     shipment_id, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shipment_id, *args, **kwargs) -> Response:
        """
        Handle DELETE requests to delete a specific shipment.

        Args:
            request: The incoming HTTP request.
            shipment_id: The ID of the shipment to delete.

        Returns:
            Response: A Response object indicating success or failure.
        """
        logger.info("DELETE request received for deleting shipment ID: %s", shipment_id)

        try:
            shipment = Shipment.objects.get(id=shipment_id)
        except ObjectDoesNotExist:
            logger.warning("Shipment with ID %s not found for deletion", shipment_id)
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

        shipment.delete()
        logger.info("Successfully deleted shipment ID: %s", shipment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
