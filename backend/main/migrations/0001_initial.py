# Generated by Django 3.2.9 on 2022-02-14 07:07

from django.db import migrations, models
import django.db.models.deletion


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
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=64, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
                'ordering': ['-created_at', '-id'],
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
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('name_local', models.CharField(max_length=64, verbose_name='Name (local)')),
                ('slug', models.SlugField(max_length=64, verbose_name='Slug')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'ordering': ['name', 'country'],
                'unique_together': {('country', 'slug')},
            },
        ),
    ]
