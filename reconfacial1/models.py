from django.db import models

class Persona(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    NOMBRE = models.CharField(max_length=100)
    APELLIDO = models.CharField(max_length=100)
    CEDULA = models.CharField(max_length=20, unique=True)
    

    def __str__(self):
        return f"{self.NOMBRE} {self.APELLIDO}"

  
