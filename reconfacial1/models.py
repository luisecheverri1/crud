from django.db import models
class Persona(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    photo_path = models.CharField(max_length=100, null=True)  

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
   
class Foto(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='fotos')
    photo_path = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.photo_path
    
class Asistencia(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    def __str__(self):
        return f"{self.persona} - {self.fecha}"
    
class ReconocimientoFacial(models.Model):
    estado = models.BooleanField(default=False)  
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.persona} - {self.estado}"