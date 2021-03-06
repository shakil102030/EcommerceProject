# Generated by Django 3.1.7 on 2021-03-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_remove_comment_blogcategry'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=190)),
                ('keywords', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='blog_category_img/')),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=30)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
