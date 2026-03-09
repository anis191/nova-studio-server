from rest_framework import serializers
from .services import pdf_to_word
from .models import Document

class PdfToWordSerializer(serializers.ModelSerializer):
    PDFTOWORD = 'PDF-To-Word'
    WORDTOPDF = 'Word-To_PDF'
    CHOICES_CONVERSION = [
        (PDFTOWORD, 'PDF-To-Word'),
        (WORDTOPDF, 'Word-To_PDF'),
    ]
    convert = serializers.ChoiceField(choices=CHOICES_CONVERSION, write_only=True, default=PDFTOWORD)
    class Meta:
        model = Document
        fields = ['id','pdf','word','convert','created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        conversion_type = validated_data.get('convert')
        if(conversion_type == self.PDFTOWORD):
            pdf_file = validated_data.get('pdf')
            document = Document.objects.create(pdf=pdf_file)
            word_file = pdf_to_word(pdf_file=pdf_file)
            document.word.save(word_file.name, word_file)
            document.save()
            print("Created!")
            return document
        raise serializers.ValidationError("Invalid conversion type")
