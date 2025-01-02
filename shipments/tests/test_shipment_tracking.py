from rest_framework.test import APITestCase
from rest_framework import status
from shipments.models import Shipment
from weather.weather import WeatherService
from django.urls import reverse

class ShipmentTrackingTests(APITestCase):
    """
    Test suite for retrieving shipment and weather data.
    """
    
    databases = {'default'}
    
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
        self.tracking_url = reverse('shipment-tracking', kwargs={'version': 'v1', 'tracking_number': self.shipment.tracking_number})

    def test_get_shipment_tracking(self):
        """
        Test GET request to track a shipment and fetch weather data.
        """
        # Assuming weather data is fetched successfully
        response = self.client.get(self.tracking_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('shipment', response.data)
        self.assertIn('weather', response.data)
        self.assertEqual(response.data['shipment']['tracking_number'], 'TN12345678')
