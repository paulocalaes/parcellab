from rest_framework.test import APITestCase
from rest_framework import status
from shipments.models import Shipment
from articles.models import Article
from django.urls import reverse

class ShipmentListTests(APITestCase):
    """
    Test suite for listing and creating shipments.
    """
    
    databases = {'default','replica'}
    
    def setUp(self):
        # Setup test data for creating and listing shipments
        self.create_url = reverse('shipment-list', kwargs={'version': 'v1'}) 
        self.list_url = reverse('shipment-list',  kwargs={'version': 'v1'})
        self.shipment_data = {
            'tracking_number': 'TN12345678',
            'carrier': 'DHL',
            'sender_address': 'Sender Address',
            'receiver_address': 'Receiver Address',
            'status': 'in-transit',
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
        

    def test_create_shipment(self):
        """
        Test POST request to create a new shipment.
        """
        response = self.client.post(self.create_url, self.shipment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tracking_number'], 'TN12345678')

    def test_list_shipments(self):
        """
        Test GET request to list all shipments.
        """
        response = self.client.post(self.create_url, self.shipment_data, format='json')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 shipment created
