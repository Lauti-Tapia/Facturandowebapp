from django.shortcuts import render
from django.http import HttpResponse

# Asegúrate de que la importación es correcta
from .services import pdf_processor

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf_file')

        if uploaded_file:
            # Y que la llamada a la función es correcta
            pdf_processor.handle_uploaded_pdf(uploaded_file)
            
            return HttpResponse(f"Archivo '{uploaded_file.name}' recibido y pasado al procesador.")
        else:
            return HttpResponse("Error: No se seleccionó ningún archivo.")

    return render(request, 'core/home.html')