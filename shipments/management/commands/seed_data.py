# shipments/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from shipments.models import Shipment
from articles.models import Article

class Command(BaseCommand):
    help = "Seed the database with shipment and article data"

    def country_code(self, country):
        country_codes = {
            'Germany': 'de',
            'France': 'fr',
            'Belgium': 'be',
            'Spain': 'es',
            'Netherlands': 'nl',
            'Denmark': 'dk',
        }
        return country_codes.get(country, 'DE')

    def handle(self, *args, **kwargs):
        # Seed data (provided in the problem statement)
        data = [
            ('TN12345678', 'DHL', 'Street 1, 10115 Berlin, Germany', 'Street 10, 75001 Paris, France', 'Laptop', 1, 800, 'LP123', 'in-transit'),
            ('TN12345678', 'DHL', 'Street 1, 10115 Berlin, Germany', 'Street 10, 75001 Paris, France', 'Mouse', 1, 25, 'MO456', 'in-transit'),
            ('TN12345679', 'UPS', 'Street 2, 20144 Hamburg, Germany', 'Street 20, 1000 Brussels, Belgium', 'Monitor', 2, 200, 'MT789', 'inbound-scan'),
            ('TN12345680', 'DPD', 'Street 3, 80331 Munich, Germany', 'Street 5, 28013 Madrid, Spain', 'Keyboard', 1, 50, 'KB012', 'delivery'),
            ('TN12345680', 'DPD', 'Street 3, 80331 Munich, Germany', 'Street 5, 28013 Madrid, Spain', 'Mouse', 1, 25, 'MO456', 'delivery'),
            ('TN12345681', 'FedEx', 'Street 4, 50667 Cologne, Germany', 'Street 9, 1016 Amsterdam, Netherlands', 'Laptop', 1, 900, 'LP345', 'transit'),
            ('TN12345681', 'FedEx', 'Street 4, 50667 Cologne, Germany', 'Street 9, 1016 Amsterdam, Netherlands', 'Headphones', 1, 100, 'HP678', 'transit'),
            ('TN12345682', 'GLS', 'Street 5, 70173 Stuttgart, Germany', 'Street 15, 1050 Copenhagen, Denmark', 'Smartphone', 1, 500, 'SP901', 'scanned'),
            ('TN12345682', 'GLS', 'Street 5, 70173 Stuttgart, Germany', 'Street 15, 1050 Copenhagen, Denmark', 'Charger', 1, 20, 'CH234', 'scanned'),
        ]

        # Iterate over the seed data and insert into the database
        for entry in data:
            tracking_number, carrier, sender_address, receiver_address, article_name, quantity, price, SKU, status = entry
            receiver_country = receiver_address.split(', ')[-1]
            receiver_zip_code = receiver_address.split(', ')[-2].split(' ')[0]

            receiver_country_code = self.country_code(receiver_country)

            # Create or update the Shipment
            shipment, created = Shipment.objects.get_or_create(
                tracking_number=tracking_number,
                carrier=carrier,
                sender_address=sender_address,
                receiver_address=receiver_address,
                status=status,
                receiver_zip_code=receiver_zip_code,
                receiver_country_code=receiver_country_code,
            )

            # Create Article linked to the Shipment
            Article.objects.create(
                shipment=shipment,
                article_name=article_name,
                quantity=quantity,
                price=price,
                SKU=SKU,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
