from rest_framework import serializers
from keep_note.models import Note, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name','slug']
        read_only_fields = ['slug']

class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    add_tag = serializers.CharField(write_only=True)
    class Meta:
        model = Note
        fields = ['id','owner','title','content','tags','add_tag','is_pinned','is_archived','is_trashed','reminder_at','created_at','updated_at']
        read_only_fields = ['owner','created_at', 'updated_at']
    
    def create(self, validated_data):
        tag = validated_data.pop('add_tag', "")
        instance = Note.objects.create(owner=self.context.get('user'), **validated_data)
        all_tag = [t.strip() for t in tag.split(',') if t.strip()]
        for t in all_tag:
            tag_obj, created = Tag.objects.get_or_create(name=t)
            instance.tags.add(tag_obj)
        return instance


