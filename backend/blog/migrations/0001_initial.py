# Generated by Django 3.2.9 on 2022-05-25 08:43

import blog.utilities
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import main.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=blog.utilities.get_article_path, verbose_name='File')),
            ],
            options={
                'verbose_name': 'Image of Article',
                'verbose_name_plural': 'Images of Articles',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
                ('image', models.ImageField(upload_to=blog.utilities.get_article_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('content', models.TextField(verbose_name='Content')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Published at')),
                ('num_views', models.IntegerField(default=0, verbose_name='Number of views')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('categories', models.ManyToManyField(to='blog.Category', verbose_name='Categories')),
                ('hashtags', models.ManyToManyField(blank=True, to='main.Hashtag', verbose_name='Hashtags')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-published_at', '-id'],
            },
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('ru', 'Русский'), ('be', 'Беларуская'), ('uk', 'Українська')], max_length=2, verbose_name='Language')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Category Translation',
                'verbose_name_plural': 'Category Translations',
                'ordering': ['category', 'language'],
                'unique_together': {('category', 'language')},
            },
        ),
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('ru', 'Русский'), ('be', 'Беларуская'), ('uk', 'Українська')], max_length=2, verbose_name='Language')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
                ('content', models.TextField(verbose_name='Content')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.article', verbose_name='Article')),
            ],
            options={
                'verbose_name': 'Article Translation',
                'verbose_name_plural': 'Article Translations',
                'ordering': ['article', 'language'],
                'unique_together': {('article', 'language')},
            },
        ),
    ]
