import json
import pymysql
import os
import datetime

# conexión a la base de datos
def get_connection():
    # Retorna una conexión a la base de datos
    return pymysql.connect(
        host=os.getenv("DB_HOST", "database-1.c1g2uk2iczzf.us-east-2.rds.amazonaws.com"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "bigotes007"),
        database=os.getenv("DB_NAME", "inventario_db"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Función principal que maneja las solicitudes de API
def lambda_handler(event, context):
    print(event)
    try:
        if "httpMethod" not in event:
            return response(400, {"error": "Falta 'httpMethod' en el evento de entrada"})

        # Obtener el método HTTP y la ruta de la solicitud
        http_method = event["httpMethod"]
        path = event.get("path", "")

        # Obtener el cuerpo de la solicitud en caso de que sea POST, PUT o DELETE
        body = json.loads(event.get("body", "{}")) if http_method in ["POST", "PUT", "DELETE"] else {}

        # Manejo de recursos según la ruta
        if "/products" in path:
            if http_method == "GET":
                return get_products()
            elif http_method == "POST":
                return create_product(body)
            elif http_method == "PUT":
                return update_product(body)
            elif http_method == "DELETE":
                return delete_product(body)

        elif "/categories" in path:
            if http_method == "GET":
                return get_categories()
            elif http_method == "POST":
                return create_category(body)
            elif http_method == "PUT":
                return update_category(body)
            elif http_method == "DELETE":
                return delete_category(body)

        elif "/providers" in path:
            if http_method == "GET":
                return get_providers()
            elif http_method == "POST":
                return create_provider(body)
            elif http_method == "PUT":
                return update_provider(body)
            elif http_method == "DELETE":
                return delete_provider(body)

        elif "/purchase_orders" in path:
            if http_method == "GET":
                return get_purchase_orders()
            elif http_method == "POST":
                return create_purchase_order(body)
            elif http_method == "PUT":
                return update_purchase_order(body)
            elif http_method == "DELETE":
                return delete_purchase_order(body)

        elif "/purchase_order_detail" in path:
            if http_method == "GET":
                return get_purchase_order_detail()
            elif http_method == "POST":
                return create_purchase_order_detail(body)
            elif http_method == "PUT":
                return update_purchase_order_detail(body)
            elif http_method == "DELETE":
                return delete_purchase_order_detail(body)

        return response(400, {"message": "Ruta o método no válido"})

    except Exception as e:
        return response(500, {"error": str(e)})

# Funciones para manejar las categorías
def get_categories():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
    connection.close()
    # Convertir fechas a formato ISO
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

# Funciones para manejar los productos
def get_products():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    connection.close()
    # Convertir fechas a formato ISO
    for prod in products:
        for key, value in prod.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                prod[key] = value.isoformat()
    return response(200, products)

def create_product(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = ("INSERT INTO products (name, description, category_id, created_at, created_by) "
               "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(sql, (
            data["name"],
            data["description"],
            data["category_id"],
            datetime.datetime.now(),
            data["created_by"]
        ))
        connection.commit()
    connection.close()
    return response(201, {"message": "Producto creado con éxito"})

def update_product(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = ("UPDATE products SET name=%s, description=%s, category_id=%s WHERE id=%s")
        cursor.execute(sql, (
            data["name"],
            data["description"],
            data["category_id"],
            data["id"]
        ))
        connection.commit()
    connection.close()
    return response(200, {"message": "Producto actualizado"})

def delete_product(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM products WHERE id=%s"
        cursor.execute(sql, (data["id"],))
        connection.commit()
    connection.close()
    return response(200, {"message": "Producto eliminado"})

# Funciones para manejar los proveedores
def get_providers():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM providers")
        result = cursor.fetchall()
    connection.close()
    return response(200, result)

def create_provider(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO providers (name, full_address, created_at, created_by) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (
            data["name"],
            data["full_address"],
            data["created_at"],
            data["created_by"]
        ))
        connection.commit()
    connection.close()
    return response(201, {"message": "Proveedor creado con éxito"})

def update_provider(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE providers SET name=%s, full_address=%s WHERE id=%s"
        cursor.execute(sql, (
            data["name"],
            data["full_address"],
            data["id"]
        ))
        connection.commit()
    connection.close()
    return response(200, {"message": "Proveedor actualizado"})

def delete_provider(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM providers WHERE id=%s"
        cursor.execute(sql, (data["id"],))
        connection.commit()
    connection.close()
    return response(200, {"message": "Proveedor eliminado"})

# Funciones para manejar las órdenes de compra
def get_purchase_orders():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM purchase_orders")
        result = cursor.fetchall()
    connection.close()
    return response(200, result)

def create_purchase_order(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO purchase_orders (provider_id, date, total, created_at, created_by) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data["provider_id"],
            data["date"],
            data["total"],
            data["created_at"],
            data["created_by"]
        ))
        connection.commit()
    connection.close()
    return response(201, {"message": "Orden de compra creada"})

def update_purchase_order(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE purchase_orders SET provider_id=%s, date=%s, total=%s WHERE id=%s"
        cursor.execute(sql, (
            data["provider_id"],
            data["date"],
            data["total"],
            data["id"]
        ))
        connection.commit()
    connection.close()
    return response(200, {"message": "Orden de compra actualizada"})

def delete_purchase_order(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM purchase_orders WHERE id=%s"
        cursor.execute(sql, (data["id"],))
        connection.commit()
    connection.close()
    return response(200, {"message": "Orden de compra eliminada"})

# Funciones para manejar los detalles de las órdenes de compra
def get_purchase_order_detail():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM purchase_order_detail")
        result = cursor.fetchall()
    connection.close()
    return response(200, result)

def create_purchase_order_detail(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO purchase_order_detail (purchase_order_id, product_id, quantity, total, created_at, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data["purchase_order_id"],
            data["product_id"],
            data["quantity"],
            data["total"],
            data["created_at"],
            data["created_by"]
        ))
        connection.commit()
    connection.close()
    return response(201, {"message": "Detalle de orden de compra creado"})

def update_purchase_order_detail(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE purchase_order_detail SET purchase_order_id=%s, product_id=%s, quantity=%s, total=%s WHERE id=%s"
        cursor.execute(sql, (
            data["purchase_order_id"],
            data["product_id"],
            data["quantity"],
            data["total"],
            data["id"]
        ))
        connection.commit()
    connection.close()
    return response(200, {"message": "Detalle de orden actualizado"})

def delete_purchase_order_detail(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM purchase_order_detail WHERE id=%s"
        cursor.execute(sql, (data["id"],))
        connection.commit()
    connection.close()
    return response(200, {"message": "Detalle de orden eliminado"})

# Función para crear una respuesta JSON estandarizada
def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body, default=str)
    }
