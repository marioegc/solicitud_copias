from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pymysql.cursors
from datetime import datetime


app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(host='192.168.1.30',
                           user='cola',
                           password='sabritas',
                           db='cola',
                           cursorclass=pymysql.cursors.DictCursor)



# Definición de la función que maneja las rutas / y /tareas/1
def index_or_first_page():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Asume que quieres la primera página de resultados, ajusta según necesidad
            pagina = 1
            sql = "SELECT id, id_audiencia_j360, texto, estado, archivo_copia FROM tareas WHERE folder = 200 ORDER BY id DESC LIMIT %s, 10"
            cursor.execute(sql, (pagina-1)*10)
            result = cursor.fetchall()
    finally:
        connection.close()

    return render_template('tareas.html', tareas=result, pagina=pagina)

# Asignación de la función de vista a las rutas / y /tareas/1
app.route('/', methods=['GET'])(index_or_first_page)
app.route('/tareas/1', methods=['GET'])(index_or_first_page)

@app.route('/tareas')
@app.route('/tareas/<int:pagina>')
def tareas(pagina=1):
    tamanio_pagina = 100  # Define cuántos elementos quieres por página
    offset = (pagina - 1) * tamanio_pagina
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, id_audiencia_j360, texto, estado, archivo_copia FROM tareas WHERE folder = 200 ORDER BY id DESC LIMIT %s OFFSET %s"
            cursor.execute(sql, (tamanio_pagina, offset))
            result = cursor.fetchall()
    finally:
        connection.close()
    return render_template('tareas.html', tareas=result, pagina=pagina)

@app.route('/agregar', methods=['GET'])
def agregar():
    return render_template('agregar.html')


@app.route('/insertar', methods=['POST'])
def insertar():
    id_audiencia_j360 = request.form['id_audiencia_j360']
    texto = request.form['texto']
    fecha_encolamiento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    archivo = f"A_{id_audiencia_j360}.mp4"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Incluye el campo folder con un valor de 200 en la consulta
            sql = "INSERT INTO tareas (fecha_encolamiento, archivo, texto, id_audiencia_j360, folder) VALUES (%s, %s, %s, %s, 200)"
            cursor.execute(sql, (fecha_encolamiento, archivo, texto, id_audiencia_j360))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('tareas'))


@app.route('/eliminar/<int:id>')
def eliminar(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tareas WHERE id = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('tareas'))


@app.route('/encolar/<int:id>')
def encolar(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Actualiza el campo estado a 0 para la tarea con el id especificado
            sql = "UPDATE tareas SET estado = 0 WHERE id = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('tareas'))

@app.route('/descargar/<nombre_archivo>')
def descargar(nombre_archivo):
    directorio = 'copias'  # Asegúrate de que este directorio exista y contenga los archivos
    return send_from_directory(directorio, nombre_archivo, as_attachment=True)


@app.route('/buscar', methods=['GET'])
def buscar():
    id_justicia_360 = request.args.get('id_justicia_360')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, id_audiencia_j360, texto, estado, archivo_copia FROM tareas WHERE id_audiencia_j360 LIKE %s"
            cursor.execute(sql, ("%{}%".format(id_justicia_360),))
            result = cursor.fetchall()
    finally:
        connection.close()

    # Reutilizando la plantilla tareas.html con los resultados filtrados
    return render_template('tareas.html', tareas=result, pagina=1)  # Ajusta según sea necesario para la paginación


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)


