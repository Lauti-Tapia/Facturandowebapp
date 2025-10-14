# core/views.py
# core/views.py
from django.shortcuts import render

def home(request):
    # La ruta correcta, sin el "template/" al inicio
    return render(request, 'core/home.html')