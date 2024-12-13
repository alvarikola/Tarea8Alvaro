import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def ejecutar_sql(sql_text):
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()

        # Consulta SQL (por ejemplo, selecciona todos los registros de una tabla llamada usuarios)
        cursor.execute(sql_text)

        # Obtener columnas para contruir claves del JSON
        columnas = [desc[0] for desc in cursor.description]

        # Convertir resultados a JSON
        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify(empleados)

    except psycopg2.Error as e:
        print("error", e)


@app.route('/hola_mundo', methods=['GET'])
def hola_mundo():
    return jsonify({ "msg": "Hola, mundo!" }
)


@app.route('/empleado/empleados', methods=['GET'])
def obtener_lista_empleados():
    resultado1 = ejecutar_sql(
        'SELECT e.nombre AS "nombre", \'Gestor\' AS "empleado" FROM public."Empleado" e INNER JOIN public."Gestor" g ON e.id = g.empleado;'
    )
    resultado2 = ejecutar_sql(
        'SELECT e.nombre AS "nombre", \'Programador\' AS "empleado" FROM public."Empleado" e INNER JOIN public."Programador" p on e.id = p.empleado;'
    )

    resultadoFinal = resultado1.json + resultado2.json

    return jsonify(resultadoFinal)

@app.route('/proyecto/proyectos', methods=['GET'])
def obtener_proyectos():
    return ejecutar_sql(
        'SELECT * FROM public."Proyecto";'
    )


@app.route('/proyecto/proyectos_activos', methods=['GET'])
def obtener_proyectos_activos():
    return ejecutar_sql(
        'SELECT nombre, descripcion, fecha_creacion, fecha_inicio, cliente FROM public."Proyecto" WHERE fecha_finalizacion is null OR fecha_finalizacion >= CURRENT_TIMESTAMP;'
    )


@app.route('/proyecto/proyectos_gestor', methods=['GET'])
def obtener_proyectos_gestor_id():
    return ejecutar_sql(
        'SELECT nombre, descripcion, fecha_creacion, fecha_inicio, cliente FROM public."Proyecto" WHERE fecha_finalizacion = NULL;'
    )




if __name__=='__main__':
    app.run(debug=True)