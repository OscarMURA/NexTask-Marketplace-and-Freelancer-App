# Generated by Django 5.0.6 on 2024-09-05 19:48

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_remove_workexperience_freelancer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='country',
            field=django_countries.fields.CountryField(default='CO', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='freelancerprofile',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
