# Generated by Django 3.1.7 on 2021-03-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0006_auto_20210326_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='icon',
            field=models.ImageField(upload_to='images/icon_image'),
        ),
    ]