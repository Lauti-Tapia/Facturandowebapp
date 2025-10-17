# core/services/pdf_processor.py

import io
from PyPDF2 import PdfReader

# OCR (Plan B)
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

# --- Configuración opcional (ajustar según tu entorno) ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Si usás Windows para pdf2image, instalá Poppler y setea su /bin:
POPPLER_PATH = r"D:\VSCode\Release-25.07.0-0\poppler-25.07.0\Library\bin"  # e.g., r"C:\poppler-24.02.0\Library\bin"
OCR_LANG = "spa+eng"  # español + inglés
OCR_DPI = 300

# ... (tus clases de error no cambian) ...
class ValidationError(Exception): pass
class FileTooLargeError(ValidationError): pass
class InvalidFileTypeError(ValidationError): pass

# ... (tu función de validación no cambia) ...
def validate_pdf(pdf_file):
    if not pdf_file.name.lower().endswith('.pdf'):
        raise InvalidFileTypeError("Error: El archivo no es un PDF.")
    if pdf_file.size > 15 * 1024 * 1024:
        raise FileTooLargeError("Error: El archivo supera el tamaño máximo de 15 MB.")

def _extract_text_with_pypdf2(pdf_bytes: bytes) -> str:
    """
    Extrae texto usando PyPDF2. Devuelve string (posible vacío).
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))
    texto = []
    for page in reader.pages:
        texto.append(page.extract_text() or "")
    return "".join(texto)

def _ocr_pdf_images(pdf_bytes: bytes) -> str:
    """
    Convierte cada página del PDF a imagen y aplica OCR con Tesseract.
    Requiere:
      - Tesseract instalado (pytesseract)
      - Poppler (pdf2image) si tu SO lo requiere (Windows)
    """
    # 1) PDF -> lista de PIL.Image (una por página)
    images = convert_from_bytes(
        pdf_bytes,
        dpi=OCR_DPI,
        poppler_path=POPPLER_PATH  # None si Poppler está en PATH (Linux/Mac)
    )

    # 2) OCR por página
    textos = []
    for idx, img in enumerate(images, start=1):
        # Preprocesado simple: gris
        if img.mode != "L":
            img = img.convert("L")
        texto = pytesseract.image_to_string(img, lang=OCR_LANG)
        textos.append(texto.strip())
        print(f"OCR: página {idx}/{len(images)} procesada ({len(texto)} chars)")

    texto_final = "\n\n".join(t for t in textos if t)
    # Impresión en consola para verificación (requisito)
    print("==== TEXTO OBTENIDO POR OCR ====")
    print(texto_final)
    print("==== FIN TEXTO OCR ====")
    return texto_final

def handle_uploaded_pdf(pdf_file):
    """
    Función principal que orquesta el procesamiento del PDF.
    - Valida
    - Intenta extracción con PyPDF2
    - Si no hay texto, aplica OCR (Tesseract) sobre imágenes
    """
    try:
        validate_pdf(pdf_file)
        print(f"Archivo '{pdf_file.name}' validado correctamente.")

        # Leemos bytes una sola vez para reutilizar en PyPDF2 y en OCR
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        pdf_file.seek(0)

        # --- Plan A: PyPDF2 ---
        texto_completo = _extract_text_with_pypdf2(pdf_bytes)

        # --- Plan B: OCR si no hay texto útil ---
        if not texto_completo.strip():
            print("\n--- DETECCIÓN ---")
            print("El PDF parece ser una imagen. Activando OCR (Tesseract).")
            print("-----------------\n")

            texto_completo = _ocr_pdf_images(pdf_bytes)

            if not texto_completo.strip():
                # No se obtuvo nada ni con OCR
                return ("Éxito", "Se intentó OCR pero no se obtuvo texto.")

            return ("Éxito", "El texto del PDF fue extraído mediante OCR.")

        # Si PyPDF2 encontró texto
        print("\n--- TEXTO EXTRAÍDO DEL PDF (PyPDF2) ---")
        print(texto_completo)
        print("---------------------------------------\n")
        return ("Éxito", "El texto del PDF fue extraído.")

    except ValidationError as e:
        print(f"Error de validación: {e}")
        return ("Error", str(e))

    except Exception as e:
        # Importamos traceback para obtener detalles completos del error
        import traceback
        print("\n==== OCURRIÓ UN ERROR INESPERADO EN EL BACKEND ====")
        # Imprime el traceback completo en la consola para un diagnóstico detallado
        traceback.print_exc()
        print("==================================================\n")
        
        # Devolvemos un mensaje de error más informativo al frontend
        error_message = f"Error de procesamiento: {type(e).__name__}"
        return ("Error", error_message)
