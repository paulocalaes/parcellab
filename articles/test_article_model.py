from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from shipments.models import Shipment
from articles.models import Article


class ArticleModelTests(TestCase):
    """
    Test suite for the Article model.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """
        # Create a Shipment instance to associate with Article
        self.shipment = Shipment.objects.create(
            tracking_number="TN12345678",
            carrier="DHL",
            sender_address="Sender Address",
            receiver_address="Receiver Address",
            receiver_zip_code="94103",
            receiver_country_code="US",
            status="in-transit"
        )

    def test_create_article(self):
        """
        Test creating an Article instance with valid data.
        """
        # Create an Article instance
        article = Article.objects.create(
            shipment=self.shipment,
            article_name="Laptop",
            quantity=1,
            price=800.0,
            SKU="LP123"
        )

        # Ensure the article is created and has the correct attributes
        self.assertEqual(article.article_name, "Laptop")
        self.assertEqual(article.quantity, 1)
        self.assertEqual(article.price, 800.0)
        self.assertEqual(article.SKU, "LP123")
        self.assertEqual(article.shipment, self.shipment)

    def test_article_str_method(self):
        """
        Test the __str__() method of the Article model.
        """
        # Create an Article instance
        article = Article.objects.create(
            shipment=self.shipment,
            article_name="Headphones",
            quantity=2,
            price=100.0,
            SKU="HP456"
        )

        # Check if the string representation of the article matches the article_name
        self.assertEqual(str(article), "Headphones")

    def test_article_creation_without_shipment(self):
        """
        Test that an article cannot be created without a valid shipment.
        """
        # Try to create an Article without shipment
        with self.assertRaises(IntegrityError):
            Article.objects.create(
                article_name="Keyboard",
                quantity=3,
                price=50.0,
                SKU="KB789"
            )

    def test_article_invalid_quantity(self):
        """
        Test that an article cannot be created with invalid quantity (negative value).
        """
        # Try creating an Article with a negative quantity and check for ValidationError
        article = Article(
            shipment=self.shipment,
            article_name="Smartphone",
            quantity=-5,  # Invalid (negative) quantity
            price=500.0,
            SKU="SP001"
        )
        
        with self.assertRaises(ValidationError):
            article.clean()  # Manually call the clean method to validate
            article.save()  # This should raise a ValidationError

    def test_article_invalid_price(self):
        """
        Test that an article cannot be created with an invalid price (negative value).
        """
        # Try creating an Article with a negative price and check for ValidationError
        article = Article(
            shipment=self.shipment,
            article_name="Smartphone",
            quantity=5,  # Invalid (negative) quantity
            price=-500.0,
            SKU="SP001"
        )
        
        with self.assertRaises(ValidationError):
            article.clean()  # Manually call the clean method to validate
            article.save()  # This should raise a ValidationError

    def test_article_sku_length(self):
        """
        Test that the SKU field has a maximum length constraint.
        """
        long_sku = "A" * 256  # SKU longer than the maximum length
        with self.assertRaises(Exception) as context:
            Article.objects.create(
                shipment=self.shipment,
                article_name="Smartwatch",
                quantity=1,
                price=250.0,
                SKU=long_sku
            )
