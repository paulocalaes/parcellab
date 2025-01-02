from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from shipments.models import Shipment

class ShipmentModelTests(TestCase):
    """
    Test suite for the Shipment model.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """
        # Create a Shipment instance to use in the tests
        self.shipment_data = {
            'tracking_number': 'TN12345678',
            'carrier': 'DHL',
            'sender_address': 'Sender Address',
            'receiver_address': 'Receiver Address',
            'status': 'in-transit',
            'receiver_zip_code': '94103',
            'receiver_country_code': 'US'
        }

    def test_create_shipment(self):
        """
        Test creating a shipment with valid data.
        """
        # Create a Shipment instance
        shipment = Shipment.objects.create(**self.shipment_data)

        # Ensure the shipment is created and has the correct attributes
        self.assertEqual(shipment.tracking_number, 'TN12345678')
        self.assertEqual(shipment.carrier, 'DHL')
        self.assertEqual(shipment.sender_address, 'Sender Address')
        self.assertEqual(shipment.receiver_address, 'Receiver Address')
        self.assertEqual(shipment.status, 'in-transit')
        self.assertEqual(shipment.receiver_zip_code, '94103')
        self.assertEqual(shipment.receiver_country_code, 'US')

    def test_shipment_str_method(self):
        """
        Test the __str__() method of the Shipment model.
        """
        # Create a Shipment instance
        shipment = Shipment.objects.create(**self.shipment_data)

        # Check if the string representation of the shipment matches the expected format
        self.assertEqual(str(shipment), "DHL - TN12345678")

    def test_tracking_number_unique(self):
        """
        Test that the tracking_number field is unique.
        """
        # Create the first shipment
        Shipment.objects.create(**self.shipment_data)

        # Try to create a shipment with the same tracking_number, expecting an IntegrityError
        with self.assertRaises(Exception):
            Shipment.objects.create(
                tracking_number='TN12345678',
                carrier='UPS',
                sender_address='Another Address',
                receiver_address='Another Address',
                status='delivered',
                receiver_zip_code='94104',
                receiver_country_code='US'
            )

    def test_receiver_zip_code_max_length(self):
        """
        Test that the receiver_zip_code field does not exceed the maximum length of 10 characters.
        """
        long_zip_code = '94101123456'  # Zip code longer than the max length of 10
        shipment = Shipment(
                tracking_number='TN12345679',
                carrier='FedEx',
                sender_address='Sender Address',
                receiver_address='Receiver Address',
                status='delivered',
                receiver_zip_code=long_zip_code,
                receiver_country_code='US'
            )
        
        with self.assertRaises(ValidationError):
            shipment.full_clean()
            shipment.save()

    def test_receiver_country_code_max_length(self):
        """
        Test that the receiver_country_code field does not exceed the maximum length of 2 characters.
        """
        long_country_code = 'USA'  # Country code longer than the max length of 2
        shipment = Shipment(
                tracking_number='TN12345680',
                carrier='UPS',
                sender_address='Sender Address',
                receiver_address='Receiver Address',
                status='in-transit',
                receiver_zip_code='94103',
                receiver_country_code=long_country_code
            )
        
        with self.assertRaises(ValidationError):
            shipment.full_clean()
            shipment.save()

    def test_missing_required_field(self):
        """
        Test that an error is raised if a required field (like tracking_number) is missing.
        """
        # Try creating a shipment without the required 'tracking_number' field
        shipment = Shipment(
            carrier='DHL',
            sender_address='Sender Address',
            receiver_address='Receiver Address',
            status='in-transit',
            receiver_zip_code='94103',
            receiver_country_code='US'
        )

        # Validate the instance before saving it to check for required fields
        with self.assertRaises(ValidationError):
            shipment.full_clean()  # This will raise a ValidationError if required fields are missing
            shipment.save()  # If the validation passed, this would save the instance
