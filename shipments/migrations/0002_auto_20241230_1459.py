# Generated by Django 3.2.25 on 2024-12-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='receiver_country_code',
            field=models.CharField(default='de', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='receiver_zip_code',
            field=models.CharField(default=123, max_length=10),
            preserve_default=False,
        ),
    ]
