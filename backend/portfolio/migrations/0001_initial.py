# Generated by Django 3.2.9 on 2022-02-14 07:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import main.utilities
import portfolio.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('image', models.ImageField(upload_to=main.utilities.get_cover_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('num_views', models.IntegerField(default=0, verbose_name='Number of views')),
                ('rating', models.PositiveBigIntegerField(default=0, verbose_name='Rating')),
                ('hashtags', models.ManyToManyField(blank=True, to='main.Hashtag', verbose_name='Tags')),
                ('likes', models.ManyToManyField(blank=True, related_name='album_likes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.organizer', verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
                'ordering': ['-created_at', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=portfolio.utilities.get_photo_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('device', models.CharField(blank=True, max_length=128, verbose_name='Device')),
                ('f_number', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='F-number (f/)')),
                ('exposure_time', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(message='Must be entered in the format: 1/123456789.', regex='^\\d\\/\\d{1,9}$')], verbose_name='Exposure time (s)')),
                ('focal_length', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Focal length (mm)')),
                ('photographic_sensitivity', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Photographic sensitivity (ISO)')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded at')),
                ('num_views', models.IntegerField(default=0, verbose_name='Number of views')),
                ('rating', models.PositiveBigIntegerField(default=0, verbose_name='Rating')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.album', verbose_name='Album')),
                ('hashtags', models.ManyToManyField(blank=True, to='main.Hashtag', verbose_name='Tags')),
                ('likes', models.ManyToManyField(blank=True, related_name='photo_likes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.organizer', verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
                'ordering': ['-uploaded_at', '-id'],
            },
        ),
    ]
