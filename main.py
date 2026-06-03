from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from database import connection_database


app = FastAPI()

class Model_client(BaseModel):
    nombre: str
    email: str
    telefono: str
    
class Model_product(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str
    
class Model_order(BaseModel):
    cliente_id : int
    producto_id : int
    cantidad: int

# --------------------- PRODUCTS---------------------------
    
@app.get("/productos")
def productos():
    conecction = connection_database()
    with conecction.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM productos"
        )
        datos = cursor.fetchall()
    conecction.close()
    return datos

@app.get("/productos/{id}")
def producto_id(id: int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM productos WHERE id = %s",
            (id,)
        )
        datos = cursor.fetchone()
        if datos is None:
            #aca agregamos la exepcion a los errores https
            raise HTTPException(status_code=404, detail="Product not Found")
    connection.close()
    return datos

@app.post("/productos")
def agregar_producto(product_agg: Model_product):
    conecction = connection_database()
    with conecction.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "INSERT INTO productos(nombre, precio, stock, categoria) VALUES (%s, %s, %s, %s)",
            (product_agg.nombre, product_agg.precio, product_agg.stock, product_agg.categoria)
        )
        conecction.commit()
    conecction.close()
    return {"aviso": "Product added"}
    #raise HTTPException(status_code=200, detail="Product added")


@app.put("/productos/{id}")
def actualizar_producto(id: int, update_product: Model_product):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, stock = %s, categoria = %s WHERE id = %s",
            (update_product.nombre, update_product.precio, update_product.stock, update_product.categoria, id)
        )
        connection.commit()
    connection.close()
    #raise HTTPException(status_code=200, detail="info of product updated")
    return {"aviso": "info of product updated"}

@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "DELETE FROM productos WHERE id = %s",
            (id,)
        )
        # Si alguien intenta borrar el producto con id = 99999 (que no existe)
        # tu base de datos va a ejecutar el DELETE, no borrará nada, 
        # y el código responderá {"aviso": "Product was deleted"} ¡mentira!
        connection.commit()
        # Para solucionar esto, 
        # después de un UPDATE o DELETE, puedes usar (cursor.rowcount.)
        # Esto te dice a cuántas filas afectó tu comando. 
        # Si es 0, significa que el ID no existía.
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found to delete")
    connection.close()
    return {"aviso": "Product deleted"}
    #raise HTTPException(status_code=200, detail="Product deleted")


# --------------------- CLIENTS ---------------------------

@app.get("/clientes")
def clientes():
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM clientes"
        )
        datos = cursor.fetchall()
    connection.close()
    return datos

@app.get("/clientes/{id}")
def clientes_id(id:int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM clientes WHERE id = %s",
            (id,)
        )
        datos = cursor.fetchone()
        if datos is None:
            raise HTTPException(status_code=404, detail="Client not found")
    connection.close()
    return datos

@app.post("/clientes")
def agregar_cliente(agg_client:Model_client):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono) VALUES(%s, %s, %s)",
            (agg_client.nombre, agg_client.email, agg_client.telefono)
        )
        connection.commit()
    connection.close()
    return {"aviso": "Client added"}
    #raise HTTPException(status_code=200, detail="Client added")

@app.put("/clientes/{id}")
def actualizar_cliente(id: int, update_client: Model_client):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "UPDATE clientes SET nombre = %s, email = %s, telefono = %s WHERE id = %s",
            (update_client.nombre, update_client.email, update_client.telefono, id)
        )
        connection.commit()
    connection.close()
    return {"aviso": "info client updated"}
    #raise HTTPException(status_code=200, detail="info client updated")

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id,)
        )
        connection.commit()
    connection.close()
    return {"aviso": "Client deleted"}

# --------------------- ORDERS ---------------------------

@app.get("/ordenes")
def ordendes():
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM ordenes"
        )
        datos = cursor.fetchall()
    connection.close()
    return datos

@app.get("/ordenes/{id}")
def ordenes_id(id: int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM ordenes WHERE id = %s",
            (id,)
        )
        datos = cursor.fetchone()
        if datos is None:
            raise HTTPException(status_code=404, detail="Order not fount")
    return datos

@app.post("/ordenes")
def agregar_orden(agg_order: Model_order):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        # Para que el ususario no coloque el total el mismo
        # ahora el total se calcula solo
        cursor.execute(
            #Buscamos el producto
            "SELECT * FROM productos WHERE id = %s",
            (agg_order.producto_id,)
        )
        # aca lo tenemos al id y sus demas datos como el ["precio"]
        producto = cursor.fetchone()
        # aca agregamos una condicion sobre el stock y la cantidad que desea comprar el usuario
        if producto["stock"] < agg_order.cantidad:
            raise HTTPException(status_code=400, detail=f"inadequate stock. Only {producto["stock"]} available")
            #return {"aviso": f"solo disponemos de {producto["stock"]}"}
        
        # Aca actulizamos el stock osea restamos la cantidad que elije el usuario con el stock del producto
        cursor.execute(
            "UPDATE productos SET stock = stock - %s WHERE id = %s",
            (agg_order.cantidad, agg_order.producto_id)
        )
        # aca calculamos el total lo multiplicamos por la cantidad
        total = producto["precio"] * agg_order.cantidad
        cursor.execute(
            "INSERT INTO ordenes(cliente_id, producto_id, cantidad, total) VALUES(%s, %s, %s, %s)",
            (agg_order.cliente_id, agg_order.producto_id, agg_order.cantidad, total)
        )
        connection.commit()
    connection.close()
    return {"aviso": "order added"}

@app.put("/ordenes/{id}")
def actualizar_orden(id: int, update_order: Model_order):
    conecction = connection_database()
    with conecction.cursor(cursor_factory=RealDictCursor) as cursor:
        # 1. Buscar la orden actual para saber la cantidad original antes del cambio
        cursor.execute("SELECT * FROM ordenes WHERE id = %s", (id,))
        orden_actual = cursor.fetchone()
        
        if orden_actual is None:
            raise HTTPException(status_code=404, detail="Order not found to update")
        
        # 2. Devolver el stock de la cantidad original al producto temporalmente
        cursor.execute(
            "UPDATE productos SET stock = stock + %s WHERE id = %s",
            (orden_actual["cantidad"], orden_actual["producto_id"])
        )
        
        # 3. Buscar el producto para conocer su precio y el stock actualizado
        cursor.execute("SELECT * FROM productos WHERE id = %s", (update_order.producto_id,))
        producto = cursor.fetchone()
        
        if producto is None:
            raise HTTPException(status_code=404, detail="Product in order does not exist")
        
        # 4. Verificar si hay stock suficiente para la nueva cantidad elegida
        if producto["stock"] < update_order.cantidad:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Only {producto['stock']} available")
        
        # 5. Restar la nueva cantidad definitiva al stock del producto
        cursor.execute(
            "UPDATE productos SET stock = stock - %s WHERE id = %s",
            (update_order.cantidad, update_order.producto_id)
        )
        
        # 6. Calcular el nuevo total de la venta y actualizar la orden
        nuevo_total = producto["precio"] * update_order.cantidad
        cursor.execute(
            "UPDATE ordenes SET cliente_id = %s, producto_id = %s, cantidad = %s, total = %s WHERE id = %s",
            (update_order.cliente_id, update_order.producto_id, update_order.cantidad, nuevo_total, id)
        )
        conecction.commit()
        
    conecction.close()
    return {"aviso": "Order updated"}


@app.delete("/ordenes/{id}")
def eliminar_orden(id: int):
    connection = connection_database()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "DELETE FROM ordenes WHERE id = %s",
            (id,)
        )
        connection.commit()
    connection.close()
    return {"aviso": "order deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload= True)