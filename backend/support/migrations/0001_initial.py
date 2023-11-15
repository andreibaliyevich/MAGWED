# Generated by Django 3.2.18 on 2023-11-12 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.PositiveSmallIntegerField(choices=[(1, 'General questions and inquiries'), (2, 'Moderation and deletion of photos'), (3, 'Technical issues'), (4, 'Partnership and advertising'), (5, 'Message for the administration')], verbose_name='Subject')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedback list',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_uuid', models.UUIDField()),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Report list',
                'ordering': ['-created_at'],
            },
        ),
    ]
