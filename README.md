Step 1: Set Up Your Django Environment
Install Django and other necessary libraries:

bash
Copy code
pip install django pillow pytesseract
Create a Django project:

bash
Copy code
django-admin startproject ocr_project
cd ocr_project
Create a Django app:

bash
Copy code
python manage.py startapp ocr
Step 2: Configure Django Project
Update settings.py:

Add 'ocr' to the INSTALLED_APPS list.
Configure media settings to handle image uploads:
python
Copy code
INSTALLED_APPS = [
    ...
    'ocr',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
Update urls.py of the project:

Include the URLs from the ocr app and configure media serving during development:
python
Copy code
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ocr.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
Step 3: Set Up the OCR App
Create forms and models:

ocr/models.py:
python
Copy code
from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
ocr/forms.py:
python
Copy code
from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
Create views:

ocr/views.py:
python
Copy code
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def ocr_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            img = Image.open(image_upload.image.path)
            tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
            text = pytesseract.image_to_string(img, config=tessdata_dir_config)
            return render(request, 'ocr/result.html', {'text': text})
    else:
        form = ImageUploadForm()
    return render(request, 'ocr/upload.html', {'form': form})
Create URL configuration:

ocr/urls.py:
python
Copy code
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ocr_image_view, name='ocr_image_view'),
]
Create templates:

templates/ocr/upload.html:
html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Image Upload</title>
</head>
<body>
    <h2>Upload an image for OCR</h2>
    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload</button>
    </form>
</body>
</html>
templates/ocr/result.html:
html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>OCR Result</title>
</head>
<body>
    <h2>Extracted Text</h2>
    <pre>{{ text }}</pre>
    <a href="/">Upload another image</a>
</body>
</html>
Step 4: Run the Django Server
Apply migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Run the server:

bash
Copy code
python manage.py runserver
Now, you can open your browser and go to http://127.0.0.1:8000/ to upload an image and see the extracted text.

Step 5: Additional Configuration (Optional)
Static Files and Media Handling: In production, you'll need to set up proper handling for static and media files.
Security: Ensure your application is secure by following Django’s security recommendations.
This completes the setup for a Django project that uses Tesseract OCR to extract text from images.
