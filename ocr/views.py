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
