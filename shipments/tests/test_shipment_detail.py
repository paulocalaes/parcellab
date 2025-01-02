from rest_framework.test import APITestCase
from rest_framework import status
from shipments.models import Shipment
from django.urls import reverse

class ShipmentDetailTests(APITestCase):
    """
    Test suite for retrieving, updating, and deleting shipments.
    """
    databases = {'default', 'replica'}
    
    def setUp(self):
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Sender Address',
            receiver_address='Receiver Address',
            status='in-transit',
            receiver_zip_code='94103',
            receiver_country_code='US'
        )
        self.detail_url = reverse('shipment-detail', kwargs={'version': 'v1', 'shipment_id': self.shipment.id})
        self.updated_data = {
            'tracking_number': 'TN87654321',
            'carrier': 'FedEx',
            'sender_address': 'New Sender Address',
            'receiver_address': 'New Receiver Address',
            'status': 'delivered',
            'receiver_zip_code': '94103',
            'receiver_country_code': 'US',
            'articles': [
                {
                'article_name': 'Laptop',
                'quantity': 1,
                'price': '2.5',
                'SKU': 'SKU12345678'
                }
            ]
        }

    def test_get_shipment(self):
        """
        Test GET request to retrieve a shipment.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tracking_number'], 'TN12345678')

    def test_update_shipment(self):
        """
        Test PUT request to update a shipment completely.
        """
        response = self.client.put(self.detail_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tracking_number'], 'TN87654321')

    def test_delete_shipment(self):
        """
        Test DELETE request to remove a shipment.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
