# Generated by Django 5.0 on 2024-01-20 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_rename_reserved_lineitem_hold_lineitem_lent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecisionPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('terminal', models.BooleanField(default=False)),
            ],
        ),
    ]
