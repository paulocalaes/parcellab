# Generated by Django 3.2.25 on 2024-12-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(max_length=255, unique=True)),
                ('carrier', models.CharField(max_length=255)),
                ('sender_address', models.CharField(max_length=255)),
                ('receiver_address', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
