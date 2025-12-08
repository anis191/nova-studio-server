from django.shortcuts import render
from keep_note.models import Tag, Note
from rest_framework.viewsets import ModelViewSet
from keep_note.serializers import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from keep_note.filters import NoteFilter

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = NoteFilter
    search_fields = ['title','content','tags__name']

    def get_serializer_context(self):
        return {'user' : self.request.user}
    
    def get_queryset(self):
        return Note.objects.filter(owner = self.request.user).select_related("owner").prefetch_related("tags")
