'''
This file contains the model for the Weather app. The model is a simple one with 
the following fields:
- zip_code: A CharField with a max length of 10 characters to store the zip code.
- country_code: A CharField with a max length of 2 characters to store the country code.
The default value is 'us'.
- temperature: A FloatField to store the temperature.
- condition: A CharField with a max length of 255 characters to store the weather condition.
- last_fetched: A DateTimeField to store the last fetched timestamp.
'''
from django.db import models

class Weather(models.Model):
    '''
    Weather class is a subclass of models.Model.
    This class defines the model for the Weather app.
    '''
    zip_code = models.CharField(max_length=10)
    country_code = models.CharField(max_length=2, default='us')
    temperature = models.FloatField()
    condition = models.CharField(max_length=255)
    last_fetched = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"Weather for {self.zip_code}"
