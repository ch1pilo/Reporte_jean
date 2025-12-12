from django.db import models
from django.contrib.auth.models import User 

class Programa(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=100, unique=True) 
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='modulos') 
    nombre = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank=True)
    estatus = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.programa.nombre} - {self.nombre}"

class Inscripcion(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones') 
    
    class Meta:
        unique_together = ('programa', 'usuario') 
        verbose_name_plural = "Inscripciones"

class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)    
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=True, blank=True)
    asistio = models.BooleanField(default=False)
    def __str__(self):
        return f"Asistencia de {self.inscripcion.usuario.username} en {self.fecha}"
    
class datos_personales(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    estatus = models.BooleanField(default=True)