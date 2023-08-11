# Generated by Django 3.2.18 on 2023-08-11 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.IntegerField(choices=[(None, 'Choose rating'), (5, '5 stars'), (4, '4 stars'), (3, '3 stars'), (2, '2 stars'), (1, '1 star')], verbose_name='Rating')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_reviews', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_review'),
        ),
    ]
