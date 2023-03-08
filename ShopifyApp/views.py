from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    elementos = [1, 2, 3]
    return render(request, "main.html", {'elements': elementos})


def Catalogo(request):
    elementos = [1, 2, 3, 4]
    return render(request, "catalogo.html", {'elements': elementos})


def Orden(request):
    elementos = [1, 2, ]
    return render(request, "orden.html", {'elements': elementos})

@csrf_exempt
def OrdenesWebhook(request):
    neworder_encabezado = {}
    neworder_detalle = {}
    neworder_cliente = {}

    if request.method == 'POST':
        res = request.body.decode()
        respuesta = json.loads(res) 

        #FACTURACION.ENCABEZADO
        #ID
        neworder_encabezado['ID'] = respuesta['id'] 

        #NumeroOrden
        neworder_encabezado['NumeroOrden'] = respuesta['order_number']

        #Total
        neworder_encabezado['Total'] = respuesta['current_total_price']

        #Fecha
        neworder_encabezado['Fecha'] = respuesta['created_at']

        #Moneda
        neworder_encabezado['Moneda'] = respuesta['currency']


        
        #FACTURACION.DETALLE
        #ID
        neworder_detalle['ID'] = respuesta['line_items'][0]['id']

        #idEncabezado
        neworder_detalle['idEncabezado'] = respuesta['id']

        #ImagenURL


        #SKU
        neworder_detalle['SKU'] = respuesta['line_items'][0]['sku']

        #Nombre
        neworder_detalle['Nombre'] = respuesta['line_items'][0]['name']

        #Cantidad
        neworder_detalle['Cantidad'] = respuesta['line_items'][0]['fulfillable_quantity']

        #Precio
        neworder_detalle['Precio'] = respuesta['line_items'][0]['price']

        #Total
        neworder_detalle['Total'] = respuesta['current_total_price']

        
        
        #FACTURACION.CLIENTE
        #ID
        neworder_cliente['ID'] = respuesta['customer']['id']

        #idEncabezado
        neworder_cliente['idEncabezado'] = respuesta['id']

        #Nombre
        neworder_cliente['Nombre'] = respuesta['billing_address']['name']

        #Telefono
        neworder_cliente['Telefono'] = respuesta['billing_address']['phone']

        #Correo
        neworder_cliente['Correo'] = respuesta['customer']['email']

        #Direccion
        neworder_cliente['Direccion'] = respuesta['billing_address']['address1']

        print(neworder_encabezado)
        print("\n")
        print(neworder_detalle)
        print("\n")
        print(neworder_cliente)
        print("\n")

        # print(respuesta['billing_address'])

        
    return HttpResponse("Ordenes webhook")
