# Generated by Django 4.1.7 on 2023-10-28 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eye_care', '0002_optician_latitude_optician_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optician',
            name='website',
        ),
    ]
