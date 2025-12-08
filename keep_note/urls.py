from django.urls import path, include
from rest_framework_nested import routers
from keep_note.views import *

router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('notes', NoteViewSet, basename='note')

urlpatterns = [
    path('',include(router.urls)),
]