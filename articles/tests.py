from rest_framework.test import APITestCase
from rest_framework import status
from articles.models import Article
from shipments.models import Shipment
from django.urls import reverse


class ArticleDetailTests(APITestCase):
    """
    Test suite for retrieving, creating, updating, and deleting articles for a shipment.
    """

    def setUp(self):
        """
        Set up test data for articles and shipments.
        """
        # Create a shipment instance to associate articles with
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Sender Address',
            receiver_address='Receiver Address',
            status='in-transit',
            receiver_zip_code='94103',
            receiver_country_code='US'
        )

        # Create an article linked to the shipment
        self.article = Article.objects.create(
            article_name='Laptop',
            quantity=1,
            price=2.5,
            SKU='SKU12345678',
            shipment=self.shipment
        )

        # Define the URL for article detail (using the article's ID)
        self.detail_url = reverse('article-detail', kwargs={'version': 'v1', 'article_id': self.article.id})

    def test_get_article(self):
        """
        Test GET request to retrieve an article.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['article_name'], 'Laptop')

    def test_get_article_not_found(self):
        """
        Test GET request when the article does not exist.
        """
        invalid_url = reverse('article-detail', kwargs={'version': 'v1', 'article_id': 999999}) # Invalid article ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article not found')

    
    def test_update_article(self):
        """
        Test PUT request to update an existing article completely.
        """
        updated_data = {
            'article_name': 'Updated Laptop',
            'quantity': 2,
            'price': 3.5,
            'SKU': 'SKU87654321',
            'shipment_id': self.shipment.id
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['article_name'], 'Updated Laptop')

    def test_update_article_not_found(self):
        """
        Test PUT request when the article does not exist.
        """
        invalid_url = reverse('article-detail', kwargs={'version': 'v1', 'article_id': 999999})
        updated_data = {
            'article_name': 'Updated Laptop',
            'quantity': 2,
            'price': 3.5,
            'SKU': 'SKU87654321',
            'shipment_id': self.shipment.id
        }
        response = self.client.put(invalid_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_article(self):
        """
        Test PATCH request to partially update an article.
        """
        partial_data = {'price': 4.0}  # Only update the price
        response = self.client.patch(self.detail_url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], 4.0)

    def test_delete_article(self):
        """
        Test DELETE request to remove an article.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure the article is deleted
        self.assertRaises(Article.DoesNotExist, Article.objects.get, id=self.article.id)

    def test_delete_article_not_found(self):
        """
        Test DELETE request when the article does not exist.
        """
        invalid_url = reverse('article-detail', kwargs={'version': 'v1', 'article_id': 999999})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
