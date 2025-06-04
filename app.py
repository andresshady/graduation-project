import os
from flask import Flask, render_template, request, redirect, flash

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'hex'}

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para usar flash()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash("No se encontró el archivo.")
            return redirect(request.url)
        
        file = request.files['archivo']
        
        if file.filename == '':
            flash("No se seleccionó ningún archivo.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash(f"Archivo '{file.filename}' subido con éxito.")
            return redirect(request.url)
        else:
            flash("Solo se permiten archivos con extensión .hex.")
            return redirect(request.url)

    return render_template("index.html")