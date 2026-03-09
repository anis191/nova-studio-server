from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document

class PdfToWordConversionViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = PdfToWordSerializer