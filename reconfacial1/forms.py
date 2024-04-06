from django import forms
from reconfacial1.models import Persona

class PersonaForm(forms.ModelForm):
    photo_path = forms.CharField(max_length=200, required=False)
    class Meta:
            model = Persona
            fields = ['cedula', 'nombre', 'apellido',]