from app import db
from datetime import datetime

class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(50))
    clave = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    def __repr__(self): return f'<Estado {self.nombre}>'

class Comercio(db.Model):
    __tablename__ = 'comercio'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    rif = db.Column(db.String(20))
    direccion_fiscal = db.Column(db.Text)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self): return f'<Comercio {self.nombre}>'

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    comercio_id = db.Column(db.Integer, db.ForeignKey('comercio.id'))
    correo = db.Column(db.String(100), unique=True)
    clave = db.Column(db.String(255))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    def __repr__(self): return f'<Usuario {self.correo}>'

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    comercio_id = db.Column(db.Integer, db.ForeignKey('comercio.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50)) # 'materia_prima', 'producto_compuesto'
    unidad_medida = db.Column(db.String(20))
    stock_minimo = db.Column(db.Numeric(10, 3))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    
    # Relaciones autorreferenciales para la receta
    lotes = db.relationship('LoteInventario', backref='producto', lazy=True)
    def __repr__(self): return f'<Producto {self.nombre}>'

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    producto_final_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad_necesaria = db.Column(db.Numeric(10, 3))
    
    # Configuración de relaciones para acceder desde el producto
    producto_final = db.relationship('Producto', foreign_keys=[producto_final_id], backref='receta_como_final')
    ingrediente = db.relationship('Producto', foreign_keys=[ingrediente_id], backref='receta_como_ingrediente')
    def __repr__(self): return f'<Receta {self.id}>'

class LoteInventario(db.Model):
    __tablename__ = 'lote_inventario'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad_disponible = db.Column(db.Numeric(10, 3))
    costo_adquisicion_unitario = db.Column(db.Numeric(10, 4))
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self): return f'<Lote {self.id} - Producto {self.producto_id}>'