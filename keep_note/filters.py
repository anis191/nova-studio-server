from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, NumberFilter
from users.models import User
from keep_note.models import Note

class NoteFilter(FilterSet):
    class Meta:
        model = Note
        fields = {
            'is_archived' : ['exact'],
            'is_trashed' : ['exact'],
        }