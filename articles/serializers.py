'''
This file is used to serialize the data from the database to JSON format.
'''
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    '''
    This class is used to serialize the data from the database to JSON format.
    '''
    class Meta:
        '''
        This class is used to define the fields that are to be serialized.
        '''
        model = Article
        fields = ['article_name', 'quantity', 'price', 'SKU']
