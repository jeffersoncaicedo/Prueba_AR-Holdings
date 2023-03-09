from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .services import ShopifyAPI 
from datetime import datetime

import json
import mysql.connector



def home(request):

    compras = []

    conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'administrador',
        password = 'adminaccount12345',
        db = 'localdb'
    )

    if conexion.is_connected():
        cursor = conexion.cursor()
        cursor.execute(""" SELECT * FROM  shopifyapp_facturacionencabezado; """)
        compra = cursor.fetchall()

        cursor.execute(""" SELECT Nombre, idEncabezado_id FROM shopifyapp_facturacioncliente """)
        cliente = cursor.fetchall()

        cursor.close()
        conexion.close()

    for i in range(len(compra)):
        compras.append({
            'orden' : compra[-(i+1)][1],
            'total' : compra[-(i+1)][2],
            'fecha' : compra[-(i+1)][3].split("T")[0],
            'nombre' : cliente[i][0],
            'id_orden' : cliente[i][1]
        })
    

    return render(request, "main.html", {'compras' : compras})


def Catalogo(request):
    
    producto = []

    conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'administrador',
        password = 'adminaccount12345',
        db = 'localdb'
    )

    if conexion.is_connected():
        cursor = conexion.cursor()
        cursor.execute(""" SELECT * FROM  shopifyapp_catalogoarticulos; """)
        productos = cursor.fetchall()

        for i in range(len(productos)):
            producto.append({
                'imagen': productos[i][2],
                'nombre': productos[i][3],
                'cantidad': productos[i][4],
                'fecha': productos[i][6].split("T")[0]
            })

    return render(request, "catalogo.html", {'elements': producto})


def Orden(request, num_orden):
    imagen = []
    orden_detail = ShopifyAPI.GetOrderDetail(str(num_orden))
    total = orden_detail['order'][0]['Total']
    num_orden = orden_detail['order'][0]['NumeroOrden']
    items = orden_detail['order'][0]['items']
    images = orden_detail['order'][0]['imagen']          

    return render(request, "orden.html", {'num_orden': num_orden, 'total': total, 'items': items, 'imagen': images[2]['Feel the beats Gamma']})

@csrf_exempt
def OrdenesWebhook(request):
    facturacion_encabezado = {}
    facturacion_detalle = {}
    facturacion_cliente = {}
    
    nuevaorden_encabezado = []
    nuevaorden_detalle = []
    nuevaorden_cliente = []

    if request.method == 'POST':
        res = request.body.decode()
        response = json.loads(res) 

        #FACTURACION.ENCABEZADO
        #ID
        nuevaorden_encabezado.append({
            'ID' : response['id'],
            'NumeroOrden' :  response['order_number'],
            'Total' : response['current_total_price'],
            'Fecha' : response['created_at'],
            'Moneda' : response['currency']
        }) 


        
        #FACTURACION.DETALLE
        nuevaorden_detalle.append({
            'ID' : response['line_items'][0]['id'],
            'idEncabezado' : response['id'],
            'ImagenURL' : "",
            'SKU' : response['line_items'][0]['sku'],
            'Nombre' : response['line_items'][0]['name'],
            'Cantidad' : response['line_items'][0]['fulfillable_quantity'],
            'Precio' : response['line_items'][0]['price'],
            'Total' : response['current_total_price'],
        })

        
        
        #FACTURACION.CLIENTE
        if 'customer' in response:
            nuevaorden_cliente.append({
                'ID' : response['customer']['default_address']['customer_id'],
                'idEncabezado' : response['id'],
                'Nombre' : response['customer']['default_address']['name'],
                'Telefono' : response['customer']['default_address']['phone'],
                'Correo' : response['customer']['email'],
                'Direccion' : response['customer']['default_address']['address1']
            })
        else:
            nuevaorden_cliente.append({
                'ID' : 0,
                'idEncabezado' : response['id'],
                'Nombre' : "No customer",
                'Telefono' : "",
                'Correo' : "",
                'Direccion' : ""
            })
        
        facturacion_encabezado['headers'] = nuevaorden_encabezado
        facturacion_detalle['details'] = nuevaorden_detalle
        facturacion_cliente['clients'] = nuevaorden_cliente

        conexion = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            user = 'administrador',
            password = 'adminaccount12345',
            db = 'localdb'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute(""" UPDATE shopifyapp_facturacionencabezado
                                SET NumeroOrden=%s,Total='%s',Fecha='%s',Moneda='%s'
                                WHERE ID = %s; """ % (facturacion_encabezado['headers']['NumeroOrden'],
                                                      facturacion_encabezado['headers']['Total'],
                                                      facturacion_encabezado['headers']['Fecha'],
                                                      facturacion_encabezado['headers']['Moneda'],
                                                      facturacion_encabezado['headers']['ID'])
                           )
            
            
            cursor.execute(""" UPDATE shopifyapp_facturaciondetalle
                                SET ImagenURL='%s',SKU=%s,Nombre='%s',Cantidad='%s',Precio='%s',Total='%s'
                                WHERE ID = %s; """ % (facturacion_detalle['details']['ImagenURL'],
                                                      int(facturacion_detalle['details']['SKU']),
                                                      facturacion_detalle['details']['Nombre'],
                                                      facturacion_detalle['details']['Cantidad'],
                                                      facturacion_detalle['details']['Precio'],
                                                      facturacion_detalle['details']['Total'],
                                                      facturacion_detalle['details']['ID'])
                           )
            
            cursor.execute(""" UPDATE shopifyapp_facturacioncliente
                                SET ID=%s,Nombre='%s',Telefono='%s',Correo='%s',Direccion='%s'
                                WHERE idEncabezado_id = %s; """ % (facturacion_cliente['clients']['ID'],
                                                                   facturacion_cliente['clients']['Nombre'],
                                                                   facturacion_cliente['clients']['Telefono'],
                                                                   facturacion_cliente['clients']['Correo'],
                                                                   facturacion_cliente['clients']['Direccion'],
                                                                   facturacion_cliente['clients']['idEncabezado'])
                           )
            

            conexion.commit()
            cursor.close()
        
    return HttpResponse("Ordenes webhook")


@csrf_exempt
def ProductosWebhook(request):
    catalogo_articulos = {}
        
    producto = []
    if request.method == 'POST':
        res = request.body.decode()
        response = json.loads(res)    

        for j in range(len(response['variants'])):
            cant += response['variants'][j]['inventory_quantity']            

        #CATALOGO.ARTICULOS
        if (response['image'] != None and len(response['variants']) == 1):
            producto.append({
                'ID' : response['id'],
                'SKU' : response['variants'][-1]['sku'],
                'ImageURL' : response['image']['src'],
                'Nombre' : response['title'],
                'Cantidad' : response['variants'][0]['inventory_quantity'],
                'FechaRegistro' : response['created_at'],
                'UltimaFechaActualizacion' : response['updated_at'],
                'Sincronizado' : response['published_at'],
            })
        elif (response['image'] == None and len(response['variants']) != 1):
            producto.append({
                'ID' : response['id'],
                'SKU' : response['variants'][-1]['sku'],
                'ImageURL' : "None",
                'Nombre' : response['title'],
                'Cantidad' : str(cant),
                'FechaRegistro' : response['created_at'],
                'UltimaFechaActualizacion' : response['updated_at'],
                'Sincronizado' : response['published_at'],
            })

        catalogo_articulos['products'] = producto
        
        conexion = mysql.connector.connect(
                host = 'localhost',
                port = 3306,
                user = 'administrador',
                password = 'adminaccount12345',
                db = 'localdb'
            )

        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute(""" UPDATE shopifyapp_catalogoarticulos
                                SET SKU=%s,ImagenURL='%s',Nombre='%s',Cantidad='%s',FechaRegistro='%s',UltimaFechaActualizacion='%s',Sincronizado='%s'
                                WHERE ID = %s; """ % (catalogo_articulos['products']['SKU'],
                                                      catalogo_articulos['products']['ImagenURL'],
                                                      catalogo_articulos['products']['Nombre'],
                                                      catalogo_articulos['products']['Cantidad'],
                                                      catalogo_articulos['products']['FechaRegistro'],
                                                      catalogo_articulos['products']['UltimaFechaActualizacion'],
                                                      catalogo_articulos['products']['Sincronizado'],
                                                      catalogo_articulos['products']['ID'])
                           )

            cursor.execute(""" INSERT INTO shopifyapp_catalogologarticulos(JSON,FechaRegistro,idArticulo_id)
                                VALUES ('%s', '%s', %s);""" % (catalogo_articulos, str(datetime.now()), catalogo_articulos['products']['ID'])
                           )

            conexion.commit()
            cursor.close()
    
    return HttpResponse("Nuevo producto webhook")