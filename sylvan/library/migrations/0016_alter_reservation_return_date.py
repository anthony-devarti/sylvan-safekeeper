# Generated by Django 5.0 on 2024-01-23 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_decisionpoint_destination_on_decline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]
