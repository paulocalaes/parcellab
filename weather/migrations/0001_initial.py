# Generated by Django 3.2.25 on 2024-12-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=10)),
                ('temperature', models.FloatField()),
                ('condition', models.CharField(max_length=255)),
                ('last_fetched', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]