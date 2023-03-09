# Prueba_AR-Holdings
<h3>Instrucciones para ejecutar la solución a la prueba técnica propuesta por AR-Holdings

<br><h2>Requisitos:
<ul>
    <li>Python 3.x.x
    <li>Django 4.x.x
    <li>MySQL 
    <li>ngrok
</ul>

<br><h2>Introducción:
Para llevar a cabo la ejecución de la solución a la prueba técnica es necesario ejecutar nuestro proyecto de _Django_ en un servidor web.
<br>Con esto en mente se utilizó un servidor gratuito, como lo es _ngrok_.


<br><h2>Manejo de Base de datos:

<p>Se utilizó una base de datos MySQL con las siguientes credenciales:
<br> <code> Nombre de la DB: localdb </code>
<br><code>Puerto de la conexión: 3306 (Puerto por defecto)</code>
<br> <code>Usuario: administrador</code>
<br> <code>Contraseña: adminaccount12345</code>

<br><h2>Ejecución:

Para ejecutar la solución, en la pantalla comandos de windows (cmd), escribir el siguiente código para lanzar ngrok:

<br> <code>
_800 es el puerto por defecto del proyecto Django_
<br> ngrok http 8000
</code>

Configurar en el proyecto Django, en la sección _ALLOWED_HOSTS_ la dirección web proporcionada por ngrok:

<br> <code>
ALLOWED_HOSTS = ['7012-2800-bf0-2ad-81-7419-c34c-b141-86e1.sa.ngrok.io']
</code>

Realizar la misma configuración en el panel administrativo de _Shopify Admin_. Dentro de _Settings-Notifications_ dirigirse a la sección de _Webhooks_. Una vez ahí modificar el webhook creado con la url proporcionada por ngrok:
<br>
    <br><img src="/ShopifyApp/static/webhook_configuration.png">

A continuación ejecutar el proyecto de _Django_ con el siguiente comando:

<br> <code> python manage.py runserver </code>

