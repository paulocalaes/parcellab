'''
This file contains the serializers for the Shipments model.
The ShipmentSerializer class is a subclass of serializers.ModelSerializer.
The ShipmentSerializer class defines the fields to be serialized.
'''
from rest_framework import serializers
from articles.serializers import ArticleSerializer
from .models import Shipment
from articles.models import Article  # Import Article model


class ShipmentSerializer(serializers.ModelSerializer):
    """
    ShipmentSerializer class is a subclass of serializers.ModelSerializer.
    This class defines the fields to be serialized, including nested articles.
    """
    articles = ArticleSerializer(many=True)

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier', 'sender_address', 'receiver_address',
                  'receiver_zip_code', 'receiver_country_code', 'status', 'articles']

    def create(self, validated_data):
        """
        Create a new Shipment instance, ensuring articles are created and linked to the shipment.
        """
        # Extract the articles data from the validated data
        articles_data = validated_data.pop('articles')

        # Create the Shipment instance
        shipment = Shipment(**validated_data)
        shipment.clean()
        shipment.save()

        # Create each article and set the foreign key (shipment) correctly
        for article_data in articles_data:
            article_data['shipment'] = shipment  # Set the shipment foreign key
            Article.objects.create(**article_data)

        return shipment

    def update(self, instance, validated_data):
        """
        Update an existing Shipment instance and its related articles.
        """
        articles_data = validated_data.pop('articles', None)

        # Update the Shipment instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if articles_data:
            # Handle updating the related articles
            for article_data in articles_data:
                # Check if we are updating or creating articles here (this is simplified, consider checking if the article already exists)
                article = article_data.get('id')
                if article:
                    article_instance = Article.objects.get(id=article)
                    for attr, value in article_data.items():
                        setattr(article_instance, attr, value)
                    article_instance.save()
                else:
                    # Create new article linked to this shipment
                    article_data['shipment'] = instance
                    Article.objects.create(**article_data)

        return instance

