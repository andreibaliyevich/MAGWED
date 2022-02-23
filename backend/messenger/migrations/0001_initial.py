# Generated by Django 3.2.9 on 2022-02-20 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'ordering': ['-last_message__created_at', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('is_viewed', models.BooleanField(default=False, verbose_name='Viewed')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.chat', verbose_name='Chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['created_at', 'id'],
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message', to='messenger.message', verbose_name='Last message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Members'),
        ),
    ]