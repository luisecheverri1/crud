from django import forms
from reconfacial1.models import Persona

class PersonaForm(forms.ModelForm):
    photo_path = forms.CharField(max_length=200, required=False)
    class Meta:
            model = Persona
            fields = ['cedula', 'nombre', 'apellido',]
            error_messages = {
            'cedula': {
                'unique': "La persona con la CEDULA introducida, YA EXISTE en la base de datos.",
            },
        }