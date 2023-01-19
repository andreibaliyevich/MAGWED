# Generated by Django 3.2.9 on 2023-01-19 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_type', models.PositiveSmallIntegerField(choices=[(1, 'New follow'), (2, 'New article'), (3, 'New album'), (4, 'New photo'), (5, 'Like of album'), (6, 'Like of photo'), (7, 'Comment of article'), (8, 'Comment of album'), (9, 'Comment of photo'), (10, 'New comment'), (11, 'New review')], verbose_name='Notice type')),
                ('object_id', models.PositiveIntegerField()),
                ('viewed', models.BooleanField(default=False, verbose_name='Viewed')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Initiator')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at', '-id'],
            },
        ),
    ]
