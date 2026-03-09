from django.db import models

# Create your models here.
class Document(models.Model):
    pdf = models.FileField(upload_to='pdf_files/', null=True, blank=True)
    word = models.FileField(upload_to='word_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"
