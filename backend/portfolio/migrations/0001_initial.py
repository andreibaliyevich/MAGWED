# Generated by Django 3.2.18 on 2023-12-21 18:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import main.utilities
import portfolio.utilities
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=main.utilities.get_cover_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='Count of views')),
                ('rating', models.PositiveIntegerField(default=0, verbose_name='Rating')),
                ('editors_choice', models.BooleanField(default=False, verbose_name='Choice of Editors')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('likes', models.ManyToManyField(blank=True, related_name='album_likes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('tags', models.ManyToManyField(blank=True, to='main.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=portfolio.utilities.get_photo_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('device', models.CharField(blank=True, max_length=128, verbose_name='Device')),
                ('f_number', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='F-number (f/)')),
                ('exposure_time', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(message='Must be entered in the format: 1/123456789.', regex='^\\d\\/\\d{1,9}$')], verbose_name='Exposure time (s)')),
                ('focal_length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Focal length (mm)')),
                ('photographic_sensitivity', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Photographic sensitivity (ISO)')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Uploaded at')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='Count of views')),
                ('rating', models.PositiveIntegerField(default=0, verbose_name='Rating')),
                ('editors_choice', models.BooleanField(default=False, verbose_name='Choice of Editors')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='portfolio.album', verbose_name='Album')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('likes', models.ManyToManyField(blank=True, related_name='photo_likes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('tags', models.ManyToManyField(blank=True, to='main.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
