'''
This file is used to configure the app name for the shipments app.
'''
from django.apps import AppConfig


class ShipmentConfig(AppConfig):
    '''
    ShipmentConfig class is a subclass of AppConfig.
    This class defines the configuration for the shipments app
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shipments'
