# Generated by Django 5.0 on 2024-01-23 07:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_alter_reservation_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 23, 7, 37, 58, 286578, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]