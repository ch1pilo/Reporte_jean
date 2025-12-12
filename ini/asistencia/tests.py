from django.db import models 
from django.contrib.auth.models import User 

class Programa(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=100)

class Modulo(models.Model):
    id_programa = models.ForeignKey('Programa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)

class Inscripcion(models.Model):
    id_programa = models.ForeignKey('Programa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Asistencias(models.Model):
    id_inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)

