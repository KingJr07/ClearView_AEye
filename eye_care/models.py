from django.db import models
from django.contrib.auth.models import User
import numpy as np
from tensorflow import keras
from keras.models import load_model

# Create your models here.

class Optician(models.Model):
    name=models.CharField(max_length=255)
    prof_image = models.ImageField(upload_to="optic_images/", null=True)
    optic_id=models.IntegerField()
    description = models.TextField(null=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    license_expiration = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_date=models.DateTimeField(auto_now_add=True)
    location_description = models.TextField(null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_by=models.ForeignKey(User, related_name="Opticians", on_delete=models.CASCADE, null=True)
    class Meta:  #metadata description for the class name in plural
        ordering = ("name",) #order them by their names
        verbose_name_plural="Opticians"

    def __str__(self): #object name to be displayed
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    optician = models.OneToOneField(Optician, on_delete=models.CASCADE, null=True, blank=True)
    

class Patient(models.Model):
    # Patient Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=15)
    is_checked = models.BooleanField(default=False)
    # Eye Service Information
    eye_image = models.ImageField(upload_to='eye_images/')
    eye_condition = models.CharField(max_length=100, null=True, blank=True, default=None)
    treatment_description = models.TextField(null=True, blank=True, default=None)
    prescription = models.TextField(null=True, blank=True, default=None)
    next_appointment_date = models.DateField(null=True, blank=True, default=None)
    created_date=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User, related_name="Patients", on_delete=models.CASCADE)
    # Additional Fields (if needed)
    # insurance_info = models.CharField(max_length=100)
    # medical_history = models.TextField()
    class Meta:  #metadata description for the class name in plural
        ordering = ("first_name",) #order them by their names
        verbose_name_plural="Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    

class Contact(models.Model):
    optician=models.ForeignKey(Optician, related_name='contacts', on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='contacts')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-modified_at',)

class ContactMessage(models.Model):
    contact=models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='created_messages', on_delete=models.CASCADE)
