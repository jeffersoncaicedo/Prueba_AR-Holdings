# Generated by Django 4.1.7 on 2023-03-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopifyApp', '0002_alter_facturacioncliente_correo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogologarticulos',
            name='ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]