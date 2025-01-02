'''
This file contains the model for the shipment object. The model is a simple one with 
the following fields:
- tracking_number: A CharField with a max length of 255 characters to store the tracking number.
- carrier: A CharField with a max length of 255 characters to store the carrier name.
- sender_address: A CharField with a max length of 255 characters to store the sender address.
- receiver_address: A CharField with a max length of 255 characters to store the receiver address.
- status: A CharField with a max length of 255 characters to store the status of the shipment.
- receiver_zip_code: A CharField with a max length of 10 characters to store the receiver zip code.
- receiver_country_code: A CharField with a max length of 2 characters to store the 
receiver country code.
'''
from django.db import models
from django.core.exceptions import ValidationError

class Shipment(models.Model):
    '''
    Shipment class is a subclass of models.Model.
    This class defines the model for the Shipment object.
    '''
    tracking_number = models.CharField(max_length=255, unique=True)
    carrier = models.CharField(max_length=255)
    sender_address = models.CharField(max_length=255)
    receiver_address = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    receiver_zip_code = models.CharField(max_length=10)
    receiver_country_code = models.CharField(max_length=2)

    objects = models.Manager()

    def __str__(self):
        return f"{self.carrier} - {self.tracking_number}"

    def clean(self):
        '''
        Custom validation method to ensure that the receiver_zip_code field does not exceed
        the maximum length of 10 characters.
        '''
        if len(self.receiver_zip_code) > 10:
            raise ValidationError("Receiver zip code cannot exceed 10 characters.")
        if len(self.receiver_country_code) > 2:
            raise ValidationError("Receiver country code cannot exceed 2 characters.")
        #unique tracking number
        if Shipment.objects.filter(tracking_number=self.tracking_number).exists():
            raise ValidationError("Tracking number must be unique.")
        