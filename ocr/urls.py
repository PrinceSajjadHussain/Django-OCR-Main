from django.urls import path
from . import views

urlpatterns = [
    path('', views.ocr_image_view, name='ocr_image_view'),
]
