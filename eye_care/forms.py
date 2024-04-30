
from django import forms
from django.contrib.auth.models import User
#from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Reset
from .models import Optician, Patient, ContactMessage

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter first name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter last name',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter password',
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Repeat password',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary'),
                Reset('reset', 'Reset', css_class='btn btn-secondary')
            )
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter username',
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'form-control',
    }))


class OpticianForm(forms.ModelForm):
    class Meta:
        model = Optician
        exclude = ['created_by']  # You can specify specific fields if needed
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prof_image': forms.FileInput(attrs={'class': 'form-control'}),
            'optic_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'license_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location_description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        
          # You can specify specific fields if needed
        exclude = ['created_at', 'is_checked','created_by']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'eye_image': forms.FileInput(attrs={'class': 'form-control'}),
            'eye_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment_description': forms.Textarea(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
            'next_appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EditPatientForm(forms.ModelForm):
    class Meta:
        model=Patient
        INPUT_CLASSES= 'w-full py-4 px-6 rounded-xl border'
        fields=('eye_condition','treatment_description','prescription','next_appointment_date','is_checked')
        widgets={
            'eye_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment_description': forms.Textarea(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
            'next_appointment_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'is_checked': forms.CheckboxInput(),
        }


class EditOpticianForm(forms.ModelForm):
    class Meta:
        model=Optician
        INPUT_CLASSES= 'w-full py-4 px-6 rounded-xl border'
        fields=('prof_image','license_expiration','description','phone_number')
        widgets={
            'prof_image': forms.FileInput(attrs={'class': 'form-control'}),
            'optic_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'created_by':forms.Select(attrs={'class': 'form-control'}),
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model=ContactMessage
        fields=('content',)
        widgets={
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }