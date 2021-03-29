# Generated by Django 3.1.7 on 2021-03-26 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_bloggrid_blogcategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogCategory',
        ),
        migrations.AlterField(
            model_name='bloggrid',
            name='image',
            field=models.ImageField(upload_to='blog/blog_grid_img'),
        ),
    ]
