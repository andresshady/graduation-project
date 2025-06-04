from flask import Flask, request, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para mensajes flash

# Carpeta donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'hex'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <h1>Subir archivo .hex a la placa PIC</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file" accept=".hex" required>
      <input type="submit" value="Subir">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se seleccionó archivo')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No se seleccionó archivo')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Aquí podrías añadir código para programar la placa con el .hex
        return f'Archivo {file.filename} subido correctamente.'
    else:
        flash('Tipo de archivo no permitido. Solo .hex')
        return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)