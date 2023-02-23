# Generated by Django 3.2.9 on 2023-02-23 15:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import main.utilities
import main.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.SlugField(max_length=2, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('name_local', models.CharField(max_length=64, verbose_name='Name (local)')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['name', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('code', models.SlugField(max_length=2, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('name_local', models.CharField(max_length=64, verbose_name='Name (local)')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['name', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='Title')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='Upload JPG or PNG image. Required minimum of size 500 x 650.', upload_to=main.utilities.get_magazine_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png')), main.validators.MinimumImageSizeValidator(500, 650)], verbose_name='Image')),
                ('file', models.FileField(upload_to=main.utilities.get_magazine_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf',))], verbose_name='File')),
                ('published_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published at')),
            ],
            options={
                'verbose_name': 'Magazine',
                'verbose_name_plural': 'Magazines',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.SlugField(max_length=5, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('name_local', models.CharField(max_length=64, verbose_name='Name (local)')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='main.country', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'ordering': ['name', 'country'],
            },
        ),
    ]
