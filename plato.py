from database import db

class Plato(db.Model):
    __tablename__ = 'platos' 
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(100), nullable=False)
    imagen_blob = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, nombre, precio, tipo, imagen, blob):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.imagen = imagen
        self.imagen_blob = blob

    def convertir_a_blob(self, imagen):
        return imagen.read()
