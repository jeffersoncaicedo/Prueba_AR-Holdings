from django.shortcuts import render

def home(request):
    elementos = [1, 2, 3, 4]
    return render(request, "main.html", {'elements': elementos})


def Catalogo(request):
    elementos = [1, 2, 3, 4]
    return render(request, "catalogo.html", {'elements': elementos})


def Orden(request):
    elementos = [1, 2, ]
    return render(request, "orden.html", {'elements': elementos})
