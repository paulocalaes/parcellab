'''
This file is used to configure the app name for the articles app.
'''
from django.apps import AppConfig


class ArticleConfig(AppConfig):
    '''
    ArticleConfig class is a subclass of AppConfig.
    This class defines the configuration for the articles app
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
