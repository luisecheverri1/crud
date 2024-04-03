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
from django.contrib import admin
from django.urls import path
from reconfacial1 import views 
from django.urls import path, re_path

app_name = 'reconfacial1'



urlpatterns = [
    path('', views.home, name='home'),
    path('capturar_rostros/', views.capturar_rostros, name='capturar_rostros'),
    path('capturar_rostros_exitoso/<int:cedula>/<str:nombre>/<str:apellido>/<photo_path>/', views.capturar_rostros_exitoso, name='capturar_rostros_exitoso'),
    path('entrenandoRF/<int:cedula>/<str:nombre>/<str:apellido>/<str:photo_path>/', views.entrenandoRF, name='entrenandoRF'),
    path('reconocer/', views.reconocer, name='reconocer'),
    # Acepta cualquier cadena de caracteres como parte de photo_path
    re_path(r'^capturar_rostros_exitoso/(?P<cedula>[0-9]+)/(?P<nombre>[^/]+)/(?P<apellido>[^/]+)/(?P<photo_path>.+)/$', views.capturar_rostros_exitoso, name='capturar_rostros_exitoso'),
]


