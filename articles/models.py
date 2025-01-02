'''
This file contains the Article model which is used to store the details of 
the articles in the database.
The model has the following fields:
- shipment: A ForeignKey field to reference the Shipment model.
- article_name: A CharField to store the name of the article.
- quantity: An IntegerField to store the quantity of the article.
- price: A FloatField to store the price of the article.
- SKU: A CharField to store the Stock Keeping Unit of the article.
'''
from django.db import models
from django.core.exceptions import ValidationError
from shipments.models import Shipment  # Reference to Shipment for ForeignKey


class Article(models.Model):
    '''
    Article class is a subclass of models.Model.
    This class defines the model for the Article app.
    '''
    shipment = models.ForeignKey(Shipment, related_name='articles', on_delete=models.CASCADE)
    article_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.FloatField()
    SKU = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return str(self.article_name)

    def clean(self):
        """
        Custom validation to ensure that quantity is non-negative.
        """
        if self.quantity < 0:
            raise ValidationError({'quantity': 'Quantity cannot be negative.'})

        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})
