# Generated by Django 3.2.18 on 2023-10-02 04:29

import blog.utilities
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import main.utilities
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
                ('image', models.ImageField(upload_to=blog.utilities.get_article_path, verbose_name='Image')),
                ('thumbnail', easy_thumbnails.fields.ThumbnailerImageField(upload_to=main.utilities.get_thumbnail_path, verbose_name='Thumbnail')),
                ('content', models.TextField(verbose_name='Content')),
                ('published_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published at')),
                ('view_count', models.IntegerField(default=0, verbose_name='Count of views')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.ImageField(upload_to=blog.utilities.get_article_path, verbose_name='File')),
            ],
            options={
                'verbose_name': 'Image of Article',
                'verbose_name_plural': 'Images of Articles',
                'ordering': ['-uuid'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('code', models.CharField(choices=[(None, '(Unknown)'), ('design', 'Design'), ('fashion', 'Fashion'), ('inspiration', 'Inspiration'), ('journey', 'Journey'), ('lifestyle', 'Lifestyle'), ('photography', 'Photography'), ('technology', 'Technology'), ('wedding', 'Wedding')], max_length=16, primary_key=True, serialize=False, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(related_name='articles', to='blog.Category', verbose_name='Categories'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='main.Tag', verbose_name='Tags'),
        ),
        migrations.AddConstraint(
            model_name='articletranslation',
            constraint=models.UniqueConstraint(fields=('article', 'language'), name='unique_articletranslation'),
        ),
    ]
