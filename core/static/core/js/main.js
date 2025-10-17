// 1. Obtenemos los elementos del HTML con los que vamos a trabajar.
const fileInput = document.getElementById('pdf_file');
const initialState = document.getElementById('upload-initial-state');
const filePreview = document.getElementById('file-preview');
const fileNameSpan = document.getElementById('file-name');

// 2. Le decimos al input que nos "avise" cuando cambie (cuando se seleccione un archivo).
fileInput.addEventListener('change', function() {
    // "this.files" es la lista de archivos que el usuario seleccionó.
    // Verificamos que al menos haya seleccionado uno.
    if (this.files && this.files.length > 0) {
        // 3. Ocultamos el mensaje inicial.
        initialState.style.display = 'none';

        // 4. Escribimos el nombre del archivo en nuestro contenedor de vista previa.
        fileNameSpan.textContent = this.files[0].name;

        // 5. Mostramos el contenedor de la vista previa.
        filePreview.style.display = 'block';
    }
});