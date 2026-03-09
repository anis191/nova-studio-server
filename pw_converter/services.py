from django.core.files.base import ContentFile
from pdf2docx import Converter
from docx2pdf import convert
from io import BytesIO

def pdf_to_word(pdf_file):
    # pdf_file is an InMemoryUploadedFile or similar
    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()

    # Use BytesIO for in-memory processing
    pdf_stream = BytesIO(pdf_bytes)

    # Create Converter with stream (no filetype needed)
    cv = Converter(stream=pdf_stream)

    # Output to another BytesIO buffer
    docx_buffer = BytesIO()
    cv.convert(docx_buffer)  # Converts all pages by default
    cv.close()

    docx_buffer.seek(0)

    # Create Django ContentFile
    word_file = ContentFile(docx_buffer.read())
    word_file.name = pdf_file.name.replace('.pdf', '.docx')

    return word_file
