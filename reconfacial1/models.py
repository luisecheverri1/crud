from django.db import models
class Persona(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=False)
    # foto_path = models.CharField(max_length=100, null=True)  # Add this line

    def __str__(self):
        return f"{self.nombre} {self.apellido}"