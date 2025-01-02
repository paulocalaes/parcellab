'''
This file contains the serializer class for the Weather model.
'''

from rest_framework import serializers
from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    '''
    This class is used to serialize the Weather model.
    '''
    class Meta:
        '''
        This class is used to define the fields to be serialized.
        '''
        model = Weather
        fields = ['zip_code', 'temperature', 'condition', 'last_fetched']
