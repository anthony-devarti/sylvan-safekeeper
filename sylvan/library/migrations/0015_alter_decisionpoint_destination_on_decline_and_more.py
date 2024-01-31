# Generated by Django 5.0 on 2024-01-23 04:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_decisionpoint_destination_on_decline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisionpoint',
            name='destination_on_decline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_on_decline', to='library.reservationstatus'),
        ),
        migrations.AlterField(
            model_name='decisionpoint',
            name='destination_on_success',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_on_success', to='library.reservationstatus'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='action_required',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.decisionpoint'),
        ),
    ]
