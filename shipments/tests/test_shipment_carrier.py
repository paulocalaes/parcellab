from rest_framework.test import APITestCase
from rest_framework import status
from shipments.models import Shipment
from django.urls import reverse

class ShipmentCarrierTests(APITestCase):
    """
    Test suite for retrieving shipments based on carrier.
    """
    
    databases = {'default', 'replica'}
    
    def setUp(self):
        self.shipment_1 = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Sender Address',
            receiver_address='Receiver Address',
            status='in-transit',
            receiver_zip_code='94103',
            receiver_country_code='US'
        )
        self.shipment_2 = Shipment.objects.create(
            tracking_number='TN87654321',
            carrier='FedEx',
            sender_address='Sender Address',
            receiver_address='Receiver Address',
            status='delivered',
            receiver_zip_code='94103',
            receiver_country_code='US'
        )
        self.carrier_url = reverse('shipment-carrier', kwargs={'version': 'v1', 'carrier': 'DHL'})

    def test_get_shipments_by_carrier(self):
        """
        Test GET request to list shipments based on carrier.
        """
        response = self.client.get(self.carrier_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)  # Only one shipment with DHL carrier
        self.assertEqual(response.data['data'][0]['tracking_number'], 'TN12345678')
