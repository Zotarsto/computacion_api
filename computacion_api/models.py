from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"

#Agregagamos el campo de Adminisitrador
class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    #Nombre, Apellido correo y contraseña se guardan en User
    clave_admin = models.CharField(max_length=255, null=True, blank=True) #ID (EN CAMPO de formulario)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    #Para cambios se realiza estas variables para determinar las fechas de creacion y actualizacion
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil de admin "+self.usuario.first_name+" "+self.usuario.last_name

#Ahora agregaremos los clases de Alumno y maestro
class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    #Nombre, Apellido correo y contraseña se guardan en User
    clave_alumno = models.CharField(max_length=255, null=True, blank=True) #ID (EN CAMPO de formulario)
    fecha_de_nacimiento = models.DateTimeField(null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    #Para cambios se realiza estas variables para determinar las fechas de creacion y actualizacion
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil de alumno "+self.usuario.first_name+" "+self.usuario.last_name

#Maestro
class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    #Nombre, Apellido correo y contraseña se guardan en User
    clave_maestro = models.CharField(max_length=255, null=True, blank=True) #ID (EN CAMPO de formulario)
    fecha_de_nacimiento = models.DateTimeField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    cubiculo = models.IntegerField(null=True, blank=True) #Los cubiulos solo son enteros
    #Los valores de las opciones son enviadas como cadenas de texto debido a los archivos .ts que se encuentran en el front
    area_investigacion = models.CharField(max_length=255, null=True, blank=True) 
    materias_json =models.TextField(null=True, blank=True) 
    #Para cambios se realiza estas variables para determinar las fechas de creacion y actualizacion
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil de maestro "+self.usuario.first_name+" "+self.usuario.last_name