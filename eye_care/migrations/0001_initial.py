# Generated by Django 4.1.7 on 2023-10-28 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Optician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('optic_id', models.IntegerField()),
                ('address', models.TextField()),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('license_expiration', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Opticians',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('registration_date', models.DateField()),
                ('eye_image', models.ImageField(upload_to='images/')),
                ('eye_condition', models.CharField(max_length=100)),
                ('treatment_description', models.TextField(blank=True, default=None, null=True)),
                ('prescription', models.TextField(blank=True, default=None, null=True)),
                ('next_appointment_date', models.DateField(blank=True, default=None, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Patients', to=settings.AUTH_USER_MODEL)),
                ('optician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Patients', to='eye_care.optician')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Patients',
                'ordering': ('optician',),
            },
        ),
    ]
