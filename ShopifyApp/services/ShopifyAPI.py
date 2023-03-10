import requests


headers = {'X-Shopify-Access-Token': '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'}
url_base = "https://ar-holdings-dev-test.myshopify.com/admin/api/2023-01/"
imagen_produco = []


def GetProductos():
    catalogo_articulos = {}
        
    producto = []

    url = url_base + 'products.json'
    get = requests.get(url, headers=headers)
    response = get.json()['products']

    for i in range(len(response)):
        cant = 0

        for j in range(len(response[i]['variants'])):
            cant += response[i]['variants'][j]['inventory_quantity']            

        #CATALOGO.ARTICULOS
        if (response[i]['image'] != None and len(response[i]['variants']) == 1):
            producto.append({
                'ID' : response[i]['id'],
                'SKU' : response[i]['variants'][-1]['sku'],
                'ImageURL' : response[i]['image']['src'],
                'Nombre' : response[i]['title'],
                'Cantidad' : response[i]['variants'][0]['inventory_quantity'],
                'FechaRegistro' : response[i]['created_at'],
                'UltimaFechaActualizacion' : response[i]['updated_at'],
                'Sincronizado' : response[i]['published_at'],
            })
            imagen_produco.append({
                response[i]['title'] : response[i]['image']['src']
            })
        elif (response[i]['image'] == None and len(response[i]['variants']) != 1):
            producto.append({
                'ID' : response[i]['id'],
                'SKU' : response[i]['variants'][-1]['sku'],
                'ImageURL' : "None",
                'Nombre' : response[i]['title'],
                'Cantidad' : str(cant),
                'FechaRegistro' : response[i]['created_at'],
                'UltimaFechaActualizacion' : response[i]['updated_at'],
                'Sincronizado' : response[i]['published_at'],
            })
            imagen_produco.append({
                response[i]['title'] : "None"
            })

    catalogo_articulos['products'] = producto
    return catalogo_articulos



def GetOrdenes():
    facturacion_encabezado = {}
    facturacion_detalle = {}
    facturacion_cliente = {}

    orden_encabezado = []
    orden_detalle = []
    orden_cliente = []

        
    url = url_base + 'orders.json'
    get = requests.get(url, headers=headers)
    response = get.json()['orders']

    for i in range(len(response)):

        #FACTURACION.ENCABEZADO
        orden_encabezado.append({
            'ID' : response[i]['id'],
            'NumeroOrden' :  response[i]['order_number'],
            'Total' : response[i]['current_total_price'],
            'Fecha' : response[i]['created_at'],
            'Moneda' : response[i]['currency']
        })    
        
        
        # #FACTURACION.DETALLE
        orden_detalle.append({
            'ID' : response[i]['line_items'][0]['id'],
            'idEncabezado' : response[i]['id'],
            'ImagenURL' : "",
            'SKU' : response[i]['line_items'][0]['sku'],
            'Nombre' : response[i]['line_items'][0]['name'],
            'Cantidad' : response[i]['line_items'][0]['fulfillable_quantity'],
            'Precio' : response[i]['line_items'][0]['price'],
            'Total' : response[i]['current_total_price'],
        })

            
        # #FACTURACION.CLIENTE
        if 'customer' in response[i]:
            orden_cliente.append({
                'ID' : response[i]['customer']['default_address']['customer_id'],
                'idEncabezado' : response[i]['id'],
                'Nombre' : response[i]['customer']['default_address']['name'],
                'Telefono' : response[i]['customer']['default_address']['phone'],
                'Correo' : response[i]['customer']['email'],
                'Direccion' : response[i]['customer']['default_address']['address1']
            })
        else:
            orden_cliente.append({
                'ID' : 0,
                'idEncabezado' : response[i]['id'],
                'Nombre' : "No customer",
                'Telefono' : "",
                'Correo' : "",
                'Direccion' : ""
            })
            
        
    facturacion_encabezado['headers'] = orden_encabezado
    facturacion_detalle['details'] = orden_detalle
    facturacion_cliente['clients'] = orden_cliente
    
    return facturacion_encabezado, facturacion_detalle, facturacion_cliente


def GetOrderDetail(id_order):
    orden_detalle = {}

    item = []
    orden = []

    url = url_base + 'orders/' + id_order + '.json'
    get = requests.get(url, headers=headers)
    response = get.json()['order']
        
    for i in range(len(response['line_items'])):

        if len(response['line_items']) == 1:
            item.append({
                'Nombre' : response['line_items'][0]['name'],
                'Cantidad' : response['line_items'][0]['fulfillable_quantity'],
                'Precio' : response['line_items'][0]['price'],
            })        
        else:
            item.append({
                'Nombre' : response['line_items'][i]['name'],
                'Cantidad' : response['line_items'][i]['fulfillable_quantity'],
                'Precio' : response['line_items'][i]['price'],
            })
    
    orden.append({
        'NumeroOrden' : response['order_number'],
        'items' : item,
        'Total' : response['current_total_price'],
        'imagen': imagen_produco
    })

    orden_detalle['order'] = orden
    return orden_detalle