import os
from flask import flash, redirect, render_template, request, url_for
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


def get_default_comercio_and_estado():
    """Obtiene o crea el estado y comercio por defecto."""
    estado = Estado.query.filter_by(clave='activo').first()
    if not estado:
        estado = Estado(entidad='global', clave='activo', nombre='Activo')
        db.session.add(estado)
        db.session.commit()

    comercio = Comercio.query.filter_by(nombre='Comercio de Prueba').first()
    if not comercio:
        comercio = Comercio(
            nombre='Comercio de Prueba',
            rif='J-00000000-0',
            direccion_fiscal='Dirección de prueba',
            estado=estado,
        )
        db.session.add(comercio)
        db.session.commit()

    return estado, comercio


@app.route('/')
def index():
    if request.args.get('add_test'):
        create_test_product()
        return redirect(url_for('index'))

    productos = Producto.query.all()
    return render_template('index.html', title='Inventario de Productos', productos=productos)


@app.route('/create-producto', methods=['GET', 'POST'])
def create_producto():
    estado, comercio = get_default_comercio_and_estado()
    categorias = Categoria.query.filter_by(comercio_id=comercio.id).all()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        tipo = request.form.get('tipo', 'materia_prima')
        unidad_medida = request.form.get('unidad_medida', 'Unidad')
        stock_minimo = request.form.get('stock_minimo', 0)
        categoria_id = request.form.get('categoria_id')

        if not nombre:
            flash('El nombre del producto es requerido.', 'danger')
            return redirect(url_for('create_producto'))

        # Si no existe la categoría, usamos la primera o creamos una por defecto
        if not categoria_id or not Categoria.query.get(categoria_id):
            if categorias:
                categoria = categorias[0]
            else:
                categoria = Categoria(
                    comercio=comercio,
                    nombre='General',
                    descripcion='Categoría por defecto',
                )
                db.session.add(categoria)
                db.session.commit()
        else:
            categoria = Categoria.query.get(categoria_id)

        producto = Producto(
            comercio=comercio,
            categoria=categoria,
            nombre=nombre,
            tipo=tipo,
            unidad_medida=unidad_medida,
            stock_minimo=float(stock_minimo) if stock_minimo else 0,
            estado=estado,
        )
        db.session.add(producto)
        db.session.commit()

        flash(f'Producto "{nombre}" registrado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('create_producto.html', title='Crear Producto', categorias=categorias, comercio=comercio)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
