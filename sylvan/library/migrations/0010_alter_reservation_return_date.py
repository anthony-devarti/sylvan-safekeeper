# Generated by Django 5.0 on 2024-01-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_reservation_date_created_reservation_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='return_date',
            field=models.DateTimeField(),
        ),
    ]