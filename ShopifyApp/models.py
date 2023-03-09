from django.db import models

# Create your models here.

class CatalogoArticulos(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    SKU = models.BigIntegerField()
    ImagenURL = models.URLField(max_length=500)
    Nombre = models.CharField(max_length=150)
    Cantidad = models.IntegerField()
    FechaRegistro = models.CharField(max_length=50)
    UltimaFechaActualizacion = models.CharField(max_length=50)
    Sincronizado =  models.CharField(max_length=50)


class CatalogoLogArticulos(models.Model):
    ID = models.AutoField(primary_key=True)
    idArticulo = models.ForeignKey(CatalogoArticulos, on_delete=models.CASCADE)
    JSON =  models.JSONField()
    FechaRegistro =  models.CharField(max_length=50)


class FacturacionEncabezado(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    NumeroOrden = models.IntegerField()
    Total = models.CharField(max_length=50) 
    Fecha = models.CharField(max_length=50)
    Moneda = models.CharField(max_length=5)

class FacturacionDetalle(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    idEncabezado = models.ForeignKey(FacturacionEncabezado, on_delete=models.CASCADE)
    ImagenURL = models.URLField(max_length=500)
    SKU = models.BigIntegerField()
    Nombre = models.CharField(max_length=150)
    Cantidad = models.CharField(max_length=10)
    Precio = models.CharField(max_length=50)
    Total = models.CharField(max_length=50)

class FacturacionCliente(models.Model):
    ids = models.AutoField(primary_key=True, blank=True)
    ID = models.BigIntegerField(blank=True)
    idEncabezado = models.ForeignKey(FacturacionEncabezado, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=150, blank=True)
    Telefono = models.CharField(max_length=50, blank=True)
    Correo = models.CharField(max_length=150, blank=True)
    Direccion = models.CharField(max_length=300, blank=True)