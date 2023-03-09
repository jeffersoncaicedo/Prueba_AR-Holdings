import mysql.connector
from .services import ShopifyAPI

try:
    
    catalogo_productos = ShopifyAPI.GetProductos()
    facturacion_encabezado, facturacion_detalles, facturacion_cliente = ShopifyAPI.GetOrdenes()

    conexion =  mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'administrador',
        password = 'adminaccount12345',
        db = 'localdb'
    )

    if conexion.is_connected():

        #CATALOGO.ARTICULOS
        cursor = conexion.cursor()
        cursor.execute("""SELECT COUNT(ID) 
                        FROM shopifyapp_catalogoarticulos;""")
        response = cursor.fetchall()
        if response[0][0] < len(catalogo_productos['products']):
            for i in range(len(catalogo_productos['products'])):
                id_number = catalogo_productos['products'][i]['ID']
                sku = catalogo_productos['products'][i]['SKU']
                imageurl = catalogo_productos['products'][i]['ImageURL']
                nombre = catalogo_productos['products'][i]['Nombre']
                cantidad = catalogo_productos['products'][i]['Cantidad']
                fecharegistro = catalogo_productos['products'][i]['FechaRegistro']
                ultimafecharegistro = catalogo_productos['products'][i]['UltimaFechaActualizacion']
                sincronizado = catalogo_productos['products'][i]['Sincronizado']

                cursor.execute(
                    """INSERT INTO shopifyapp_catalogoarticulos(ID,SKU,ImagenURL,Nombre,Cantidad,FechaRegistro,UltimaFechaActualizacion,Sincronizado)
                    VALUES (%s, %s, '%s', '%s', %s, '%s', '%s', '%s');""" % (id_number, 
                                                                            int(sku), 
                                                                            imageurl, 
                                                                            nombre, 
                                                                            cantidad, 
                                                                            fecharegistro, 
                                                                            ultimafecharegistro, 
                                                                            sincronizado)
                )
                conexion.commit()
        cursor.close()
        
        #FACTURACION.ENCABEZADO
        cursor = conexion.cursor()
        cursor.execute("""SELECT COUNT(ID) 
                        FROM shopifyapp_facturacionencabezado;""")
        response = cursor.fetchall()
        if response[0][0] < len(facturacion_encabezado['headers']):
            for i in range(len(facturacion_encabezado['headers'])):
                id_number_encabezado = facturacion_encabezado['headers'][i]['ID']
                numeroorden_encabezado = facturacion_encabezado['headers'][i]['NumeroOrden']
                total_encabezado = facturacion_encabezado['headers'][i]['Total']
                fecha_encabezado = facturacion_encabezado['headers'][i]['Fecha']
                moneda_encabezado = facturacion_encabezado['headers'][i]['Moneda']
            
                cursor.execute(
                    """INSERT INTO shopifyapp_facturacionencabezado(ID,NumeroOrden,Total,Fecha,Moneda)
                    VALUES (%s, %s, '%s', '%s', '%s');""" % (id_number_encabezado, 
                                                            numeroorden_encabezado, 
                                                            total_encabezado, 
                                                            fecha_encabezado, 
                                                            moneda_encabezado)
                )
                conexion.commit()
        
        cursor.close()
        
        #FACTURACION.DETALLE
        cursor = conexion.cursor()
        cursor.execute("""SELECT COUNT(ID) 
                        FROM shopifyapp_facturaciondetalle;""")
        response = cursor.fetchall()
        if response[0][0] < len(facturacion_detalles['details']):
            for i in range(len(facturacion_detalles['details'])):
                id_number = facturacion_detalles['details'][i]['ID']
                id_anterior = facturacion_detalles['details'][i]['idEncabezado']
                imagenurl = facturacion_detalles['details'][i]['ImagenURL']
                sku = facturacion_detalles['details'][i]['SKU']
                nombre = facturacion_detalles['details'][i]['Nombre']
                cantidad = facturacion_detalles['details'][i]['Cantidad']
                precio = facturacion_detalles['details'][i]['Precio']
                total = facturacion_detalles['details'][i]['Total']
                        
                cursor.execute(
                    """INSERT INTO shopifyapp_facturaciondetalle(ID,ImagenURL,SKU,Nombre,Cantidad,Precio,Total,idEncabezado_id)
                    VALUES (%s, '%s', %s, '%s', '%s', '%s', '%s', %s);""" % (id_number, 
                                                                            imagenurl, 
                                                                            int(sku), 
                                                                            nombre, 
                                                                            str(cantidad),
                                                                            precio, 
                                                                            total,
                                                                            id_anterior)
                )
                conexion.commit()
        cursor.close()
        
        #FACTURACION.CLIENTE
        cursor = conexion.cursor()
        cursor.execute("""SELECT COUNT(ID) 
                        FROM shopifyapp_facturacioncliente;""")
        response = cursor.fetchall()
        if response[0][0] < len(facturacion_cliente['clients']):
            for i in range(len(facturacion_cliente['clients'])):
                id_number = facturacion_cliente['clients'][i]['ID']
                id_anterior = facturacion_cliente['clients'][i]['idEncabezado']
                nombre = facturacion_cliente['clients'][i]['Nombre']
                telefono = facturacion_cliente['clients'][i]['Telefono']
                correo = facturacion_cliente['clients'][i]['Correo']
                direccion = facturacion_cliente['clients'][i]['Direccion']

                cursor.execute(
                    """INSERT INTO shopifyapp_facturacioncliente(ID,Nombre,Telefono,Correo,Direccion,idEncabezado_id)
                    VALUES (%s, '%s', '%s', '%s', '%s', %s);""" % (id_number, 
                                                                nombre, 
                                                                telefono, 
                                                                correo, 
                                                                direccion,
                                                                id_anterior)
                )
                conexion.commit()
        cursor.close()
    conexion.close()
except:
    print("No se pudo establecer conexión con la base de datos")