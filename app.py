import os
from flask import redirect, render_template, request, url_for
from app import create_app, db
from app.models import Categoria, Comercio, Estado, Producto

app = create_app()


def create_test_product():
    estado = Estado.query.filter_by(clave='activo').first()
    if not estado:
        estado = Estado(entidad='global', clave='activo', nombre='Activo')
        db.session.add(estado)

    comercio = Comercio.query.filter_by(nombre='Comercio de Prueba').first()
    if not comercio:
        comercio = Comercio(
            nombre='Comercio de Prueba',
            rif='J-00000000-0',
            direccion_fiscal='Dirección de prueba',
            estado=estado,
        )
        db.session.add(comercio)

    categoria = Categoria.query.filter_by(nombre='Categoría de Prueba').first()
    if not categoria:
        categoria = Categoria(
            comercio=comercio,
            nombre='Categoría de Prueba',
            descripcion='Categoría generada automáticamente para pruebas',
        )
        db.session.add(categoria)

    db.session.commit()

    producto = Producto.query.filter_by(nombre='Producto de Prueba').first()
    if not producto:
        producto = Producto(
            comercio=comercio,
            categoria=categoria,
            nombre='Producto de Prueba',
            tipo='materia_prima',
            unidad_medida='Unidad',
            stock_minimo=1,
            estado=estado,
        )
        db.session.add(producto)
        db.session.commit()

    return producto


@app.route('/')
def index():
    if request.args.get('add_test'):
        create_test_product()
        return redirect(url_for('index'))

    productos = Producto.query.all()
    return render_template('index.html', title='Inventario de Productos', productos=productos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
