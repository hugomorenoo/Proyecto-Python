from flask import render_template, send_file, url_for, request, redirect, flash
from database import app, db
import io
from datetime import datetime
from plato import Plato

@app.route('/')
def home():
    platos = Plato.query.all()
    return render_template("index.html", platos = platos)

@app.route('/alta')
def alta():
    return render_template("alta.html")

@app.route('/nuevoPlato', methods=['POST'])
def anadirPlato():
    nombre = request.form['nombre']
    precio = request.form['precio']
    tipo = request.form['tipo']
    img = request.files['imagen']

    if img.filename!= "":
        if imagen_grande(img):
            flash("La imagen es demasiado grande (máximo 64 KB)")
            return redirect(url_for('alta'))
        
        nombreFoto = guardar_imagen(img)
    else:
        flash("No hay imagen")
        return redirect(url_for('alta'))

    if nombre and precio and tipo and img:
        blob = Plato.convertir_a_blob(Plato, img)
        nuevo_plato = Plato(nombre, precio, tipo, nombreFoto, blob)
        db.session.add(nuevo_plato)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash("Debes de rellenar todos lo campos")
        return redirect(url_for('alta'))

def imagen_grande(imagen):
    tamaño_maximo = 64 * 1024 
    tamaño_imagen = len(imagen.read())
    imagen.seek(0) 

    return tamaño_imagen > tamaño_maximo

@app.route('/mostrar_imagenBlob/<int:id_plato>')
def mostrar_imagenBlob(id_plato):
    plato = Plato.query.get(id_plato)
    if plato.imagen_blob:
        return send_file(io.BytesIO(plato.imagen_blob), mimetype="image/jpeg")
    else:
        return "No se ha podido mostrar imagen", 404

def guardar_imagen(imagen):
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    nombre_foto = tiempo + imagen.filename

    return nombre_foto

@app.route('/editar_plato/<int:id>', methods=['GET', 'POST'])
def editar_plato(id):
    plato = Plato.query.get(id)

    if request.method == 'POST':
        plato.nombre = request.form['nombre']
        plato.precio = request.form['precio']
        plato.tipo = request.form['tipo']

        img = request.files.get('imagen')

        if img and img.filename != "":
            if imagen_grande(img):
                flash("La imagen es demasiado grande (máximo 64 KB)")
                return render_template('editar.html', plato=plato)

            nombre_foto = guardar_imagen(img)
            plato.imagen = nombre_foto
            plato.imagen_blob = plato.convertir_a_blob(img)

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('editar.html', plato=plato)

@app.route('/borrar_plato/<int:id>', methods=['GET', 'POST'])
def borrar_plato(id):
    plato = Plato.query.get(id)
    if plato:
        db.session.delete(plato)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)