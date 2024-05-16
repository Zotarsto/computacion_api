from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from computacion_api.serializers import *
from computacion_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import json

#Permite obtener toda la lista de materiass
class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("id")
        materias = MateriasSerializer(materias, many=True).data
        #Aquí convertimos los valores de nuevo a un array de los dias de la semana
        if not materias:
            return Response({},400)
        for materia in materias:
            materia["dias_json"] = json.loads(materia["dias_json"])

        return Response(materias, 200)

class MateriasView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        materia = MateriasSerializer(materia, many=False).data
        materia["dias_json"] = json.loads(materia["dias_json"])
        return Response(materia, 200)
    
    #Registrar nueva materia
    def post(self, request, *args, **kwargs):
        serializer = MateriasSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Validar si ya existe una materia con el mismo NRC
            existing_materia = Materias.objects.filter(nrc=validated_data['nrc']).first()
            if existing_materia:
                return Response({"message": "Materia with NRC {} already exists.".format(validated_data['dias_json'])}, status=400)
            
            #Create a profile for the Materia
            materia = Materias.objects.create(
                nrc = request.data["nrc"],
                nombre= request.data["nombre"],
                seccion= request.data["seccion"],
                dias_json = json.dumps(request.data["dias_json"]),
                horaInicio= request.data["horaInicio"],
                horaFin= request.data["horaFin"],
                salon = request.data["salon"],
                programa_educativo = request.data["programa_educativo"],
            )
                                            
            materia.save() 

            return Response({"materia_created_id": materia.id }, 201)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Se tiene que modificar la parte de edicion y eliminar
class MateriasViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        materias = get_object_or_404(Materias, id=request.data["id"])
        materias.nrc = request.data["nrc"]
        materias.nombre = request.data["nombre"]
        materias.seccion = request.data["seccion"]
        materias.dias_json = json.dumps(request.data["dias_json"])
        materias.horaInicio = request.data["horaInicio"]
        materias.horaFin = request.data["horaFin"]
        materias.salon = request.data["salon"]
        materias.programa_educativo = request.data["programa_educativo"]
        materias.save()
        return Response(MateriasSerializer(materias, many=False).data,200)
    
    #Eliminar materiass
    def delete(self, request, *args, **kwargs):
        materias = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materias.delete()
            return Response({"details":"Materias eliminada"},200)
        except Exception as e:            
            return Response({"details":"Algo paso mal al eliminar"},200)