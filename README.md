# API Lambda para Gestión de Categorías

Esta API permite gestionar categorías,producstos,proveedores,ordenes de compra y detalles de ordenes de compra con sus respectivos metodos  (GET, POST, PUT, DELETE) conectada a una base de datos MySQL en AWS RDS mediante AWS Lambda y API Gateway.

## Requisitos

- AWS Lambda con integración de proxy habilitada
- API Gateway
- Base de datos MySQL en AWS RDS

## Estructura

- `lambda_function.py`: Lógica de la función Lambda
- `requirements.txt`: Dependencias
- `.gitignore`: Archivos ignorados por Git

## Instalación y pruebas

1. Instala dependencias:

```
pip install -r requirements.txt -t .
```

2. Empaqueta y sube a Lambda.

3. Prueba en Postman usando el endpoint de API Gateway.
   Endpoint principal:

   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo

   Endpoints de recursos              (!!Remover espacios en blanco!!)
   
   Productos:
   
   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo/products
   
   Categorias:
   
   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo/categories
   
   Proveedores:
   
   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo/providers
   
   Órdenes de compra:
   
   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo/purchase_orders
   
   Detalles de orden de compra:
   
   https://oxkdhrzma6.execute-api.us-east-2.amazonaws.com/desarrollo/purchase_order_detail
   
