from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('', views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path('logout',views.logout,name='logout'),
    path('create_optician/', views.create_optician, name='create_optician'),
    path('create_patient/', views.create_patient, name='create_patient'),
    path('optician/<int:optician_id>/', views.optician_detail, name='optician_detail'),
    path('user-patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('opticians/', views.opticians, name='opticians'),
    path('<int:pk>/delete_patient/', views.delete_patient, name='delete_patient'),
    path('<int:pk>/edit_patient/', views.edit_patient, name='edit_patient'),
    path('<int:pk>/delete_optician/', views.delete_optician, name='delete_optician'),
    path('<int:pk>/edit_optician/', views.edit_optician, name='edit_optician'),
    path('contact/<int:pk>/', views.new_contact, name='new_contact'),
    path('inbox/', views.messages,name='messages' ),
    path('<int:pk>/', views.mess_detail, name='conversation'),
    path('user-patients/', views.user_patients, name='user_patients'),
    path('search/', views.search_opticians, name='search_opticians'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# add this line to display the media contents