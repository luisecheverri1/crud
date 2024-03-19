# En tu aplicación, crea un archivo forms.py
from django import forms
from reconfacial1.models import Persona

class PersonaForm(forms.Form):
    CEDULA = forms.CharField(max_length=10)
    NOMBRE = forms.CharField(max_length=100)
    APELLIDO = forms.CharField(max_length=100)