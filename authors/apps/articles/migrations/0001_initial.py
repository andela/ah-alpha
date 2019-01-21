# Generated by Django 2.1.4 on 2019-01-24 15:38

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('body', models.CharField(db_index=True, max_length=8055)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favourites', models.BooleanField(default=False)),
            ],
        ),
    ]
