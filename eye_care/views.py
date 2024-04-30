from django.shortcuts import render, redirect, get_object_or_404
from .forms import  SignupForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q 
from django.contrib import messages as django_messages
from django.http import HttpResponseServerError
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import os
from keras.models import load_model
from PIL import Image
import json
from .models import Optician, Patient, Contact, ContactMessage,UserProfile
from .forms import OpticianForm, PatientForm, EditPatientForm,EditOpticianForm, ContactMessageForm
# Create your views here.
import os

if not os.path.exists('media\\prediction'):
    os.makedirs('media\\prediction')

@csrf_protect  
def signup(request):
    # Ensuring that the form is saved
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form
    })


def logout(request):
    auth.logout(request)
    return redirect('/')


def index(requests):
    opticians=Optician.objects.all()
    return render(requests, 'index.html',{
        'opticians':opticians
        })

@login_required
def create_optician(request):
    # Attempt to get the most recent optician profile associated with the user
    try:
        optician = Optician.objects.filter(created_by=request.user).latest('created_at')
        return redirect('edit_optician', pk=optician.pk)
    except Optician.DoesNotExist:
        pass
    except Optician.MultipleObjectsReturned:
        pass
        # Handle the case where multiple optician profiles are associated with the user
        # You can display an error message or take appropriate action here

    # Corrected indentation for the following block
    if request.method == 'POST':
        form = OpticianForm(request.POST, request.FILES)
        if form.is_valid():
            optician = form.save(commit=False)
            optician.created_by = request.user
            optician.save()
            return redirect('opticians')
    else:
        form = OpticianForm()

    return render(request, 'create_optician.html', {'form': form})


@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            return redirect('user_patients')
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})


@login_required
def optician_detail(request, optician_id):
    optician = get_object_or_404(Optician, id=optician_id)
    return render(request, 'optician_detail.html', {'optician': optician})

@login_required
def patient_detail(request, patient_id):
    try:
        patient = get_object_or_404(Patient, pk=patient_id)

        if patient.eye_image:
            # Your prediction code here
            image_path = os.path.join('media', str(patient.eye_image))
            model_path = 'D:/AEye/retinal_model.h5'  # Replace with the correct path to your model

            try:
                model = load_model(model_path)
            except Exception as model_load_error:
                return HttpResponseServerError(f"Error loading the model: {model_load_error}")

            try:
                img = Image.open(image_path)
                img = img.resize((150, 150))
                img = np.array(img) / 255.0

                prediction = model.predict(np.expand_dims(img, axis=0))
                # Map predictions to labels
                predictions = prediction[0]  # Extract the first element as a list
                labels = [
                    'Disease_Risk', 'Diabetic retinopathy', 'Age-related macular degeneration', 'Media haze', 'Drusen', 'Myopia',
                    'Branch retinal vein occlusion', 'Tessellation', 'Epiretinal membrane', 'Laser scars', 'Macular scars',
                    'Central serous retinopathy', 'Optic disc cupping', 'Central retinal vein occlusion', 'Tortuous vessels',
                    'Asteroid hyalosis', 'Optic disc pallor', 'Optic disc edema', 'Optociliary shunt',
                    'Anterior ischemic optic neuropathy', 'Parafoveal telangiectasia', 'Retinal traction', 'Retinitis',
                    'Chorioretinitis', 'Exudation', 'Retinal pigment epithelium changes', 'Macular hole', 'Retinitis pigmentosa',
                    'Cotton-wool spots', 'Coloboma', 'Preretinal hemorrhage',
                    'Myelinated nerve fibers', 'Central retinal artery occlusion',
                    'Tilted disc', 'Cystoid macular edema', 'Post-traumatic choroidal rupture', 'Choroidal folds', 'Vitreous hemorrhage',
                    'Macroaneurysm', 'Vasculitis', 'Branch retinal artery occlusion', 'Plaque', 'Hemorrhagic pigment epithelial detachment',
                    'Collateral'
                ]
                # Create a list of dictionaries to hold labels and corresponding predictions
                predictions_data = [{'label': label, 'prediction': float(prob)} for label, prob in zip(labels, predictions)]

            except Exception as prediction_error:
                return HttpResponseServerError(f"Error making predictions: {prediction_error}")

        else:
            predictions_data = []

        context = {
            'patient': patient,
            'predictions_data': predictions_data,
        }

        return render(request, 'patient_detail.html', context)

    except Exception as general_error:
        return HttpResponseServerError(f"An error occurred: {general_error}")
    
@login_required
def user_patients(request):
    # Get all patients created by the currently logged-in user
    patients = Patient.objects.filter(created_by=request.user, is_checked=False).order_by('-created_date')
    query = request.GET.get('query', '')


    # You can customize the fields based on your Optician model
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(eye_condition__icontains=query) | 
            Q(next_appointment_date__icontains=query) | 
            Q(prescription__icontains=query)
        )


    context = {
        'patients': patients,
        'query': query,
    }

    return render(request, 'patient_list.html', context)

@login_required
def opticians(request):
    opticians = Optician.objects.all().order_by('?')
    query = request.GET.get('query', '')


    # You can customize the fields based on your Optician model
    if query:
        opticians = opticians.filter(
            Q(name__icontains=query) | 
            Q(created_by__username__icontains=query) | 
            Q(location_description__icontains=query) | 
            Q(email__icontains=query)
        )

    return render(request, 'opticians.html',{
        'opticians':opticians,
        'query':query
        })

@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    patient.delete()

    return redirect('user_patients')

@login_required   
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditPatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)  # Use 'patient_id' instead of 'pk'
    else:
        form = EditPatientForm(instance=patient)
    return render(request, 'create_patient.html', {
        'form': form,
    })

@login_required
def delete_optician(request, pk):
    optician = get_object_or_404(Optician, pk=pk, created_by=request.user)
    optician.delete()

    return redirect('opticians')

@login_required    
def edit_optician(request,pk):
    optician = get_object_or_404(Optician, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form=EditOpticianForm(request.POST, request.FILES, instance=optician)
        if form.is_valid():
            form.save()
            return redirect('optician_detail',pk=optician.id)
    else:
        form=EditOpticianForm(instance=optician)
    return render(request,'create_optician.html',{
        'form':form,
    })



@login_required
def new_contact(request, pk):
    optician = get_object_or_404(Optician, pk=pk)

    if optician.created_by == request.user:
        return redirect('index')

    conversations = Contact.objects.filter(optician=optician).filter(members__in=[request.user.id])

    if conversations:
        # Redirect to the existing conversation
        return redirect('conversation', pk=conversations.first().pk)

    form = ContactMessageForm()

    if request.method == 'POST':
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            conversation = Contact.objects.create(optician=optician)
            conversation.members.add(request.user)
            conversation.members.add(optician.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.contact = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Notify the user about the new message
            django_messages.success(request, 'Message sent successfully!')

            return redirect('messages')

    return render(request, 'contact.html', {'form': form})

@login_required
def messages(request):
    conversations = Contact.objects.filter(members__in=[request.user.id])
    query = request.GET.get('query', '')


    # You can customize the fields based on your Optician model
    if query:
        conversations = conversations.filter(
            Q(optician__name__icontains=query) | 
            Q(members__username__icontains=query)
        )
    return render(request, 'messages.html', {
        'conversations': conversations,
        'query': query
    })

@login_required
def mess_detail(request, pk):
    conversation = Contact.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.contact = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            conversation.save()

            # Notify the user about the new message
            django_messages.success(request, 'Message sent successfully!')

            return redirect('conversation', pk=pk)
    else:
        form = ContactMessageForm()

    return render(request, 'conversation.html', {
        'conversation': conversation,
        'form': form
        
    })


def search_opticians(request):
    query = request.GET.get('query', '')
    opticians = Optician.objects.all()

    # You can customize the fields based on your Optician model
    if query:
        opticians = opticians.filter(
            Q(name__icontains=query) | 
            Q(created_by__username__icontains=query) | 
            Q(location_description__icontains=query) | 
            Q(email__icontains=query)
        )

    return render(request, 'search_results.html', {
        'opticians': opticians,
        'query': query,
    })

