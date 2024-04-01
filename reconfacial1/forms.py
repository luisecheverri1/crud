from django import forms
from reconfacial1.models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['CEDULA', 'NOMBRE', 'APELLIDO']