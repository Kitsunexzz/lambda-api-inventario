import json
import pymysql
import os
import datetime

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "database-1.c1g2uk2iczzf.us-east-2.rds.amazonaws.com"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "bigotes007"),
        database=os.getenv("DB_NAME", "inventario_db"),
        cursorclass=pymysql.cursors.DictCursor
    )

def lambda_handler(event, context):
    print(event)
    try:
        if "httpMethod" not in event:
            return response(400, {"error": "Falta 'httpMethod' en el evento de entrada"})

        http_method = event["httpMethod"]

        if http_method == "GET":
            return get_categories()
        elif http_method == "POST":
            if "body" not in event:
                return response(400, {"error": "Falta 'body' en la petición"})
            body = json.loads(event["body"])
            return create_category(body)
        elif http_method == "PUT":
            if "body" not in event:
                return response(400, {"error": "Falta 'body' en la petición"})
            body = json.loads(event["body"])
            return update_category(body)
        elif http_method == "DELETE":
            if "body" not in event:
                return response(400, {"error": "Falta 'body' en la petición"})
            body = json.loads(event["body"])
            return delete_category(body)
        else:
            return response(400, {"message": "Método no permitido"})

    except Exception as e:
        return response(500, {"error": str(e)})

def get_categories():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
    connection.close()
    for cat in categories:
        for key, value in cat.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                cat[key] = value.isoformat()
    return response(200, categories)

def create_category(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO categories (name, description, created_by) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data["name"], data["description"], data["created_by"]))
        connection.commit()
    connection.close()
    return response(201, {"message": "Categoría creada con éxito"})

def update_category(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE categories SET name=%s, description=%s WHERE id=%s"
        cursor.execute(sql, (data["name"], data["description"], data["id"]))
        connection.commit()
    connection.close()
    return response(200, {"message": "Categoría actualizada"})

def delete_category(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM categories WHERE id=%s"
        cursor.execute(sql, (data["id"],))
        connection.commit()
    connection.close()
    return response(200, {"message": "Categoría eliminada"})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
