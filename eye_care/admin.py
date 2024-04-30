from django.contrib import admin
from .models import Optician,Patient, Contact,ContactMessage,UserProfile
# Register your models here.

admin.site.register(Optician),
admin.site.register(Patient),
admin.site.register(Contact),
admin.site.register(ContactMessage),
admin.site.register(UserProfile),