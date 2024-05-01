"""
URL configuration for biometrikAssProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Standard library imports
from django.contrib import admin
from django.urls import path, re_path

# Local application imports
from reconfacial1 import views

app_name = 'reconfacial1'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Capture faces CREATE
    path('capturar_rostros/', views.capturar_rostros, name='capturar_rostros'),

    # Capture faces successful
    path('capturar_rostros_exitoso/<int:cedula>/<str:nombre>/<str:apellido>/<path:photo_path>/<path:person_folder_path>/<int:count>/', 
        views.capturar_rostros_exitoso, name='capturar_rostros_exitoso'),

    # Train facial recognition model
    path('entrenandoRF/<str:cedula>/<str:nombre>/<str:apellido>/<path:photo_path>/<path:person_folder_path>/<int:count>/', 
        views.entrenandoRF, name='entrenandoRF'),

    # Train facial recognition model successful
    path('entrenandoRF_exitoso/<int:cedula>/<str:nombre>/<str:apellido>/<path:photo_path>/<path:person_folder_path>/<int:count>/', views.
    entrenandoRF_exitoso, name='entrenandoRF_exitoso'),



    # Recognize faces
    path('reconocerhtml/', views.reconocerhtml, name='reconocerhtml'),
    # Recognize faces
    path('reconocer_rostros/', views.reconocer_rostros, name='reconocer_rostros'),
    # Recognize faces
    path('reconociendo/', views.reconociendo, name='reconociendo'),
    


    # Read person
    path('leer_persona/<int:cedula>/', views.leer_persona, name='leer_persona'),

    # Update person
    path('actualizar_persona/<int:cedula>/', views.actualizar_persona, name='actualizar_persona'),

    # Delete person
    path('eliminar_persona/<int:cedula>/', views.eliminar_persona, name='eliminar_persona'),

    # Persona list
    path('persona_list/', views.persona_list, name='persona_list'),

    path('checking/<str:nombre>/<str:apellido>/', views.checking, name='checking'),

    path('bienvenido/<str:nombre>/<str:apellido>/', views.bienvenido, name='bienvenido'),
]
