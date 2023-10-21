# Generated by Django 3.2.18 on 2023-10-21 08:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.validators
import messenger.utilities
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chat_type', models.PositiveSmallIntegerField(choices=[(1, 'Dialog'), (2, 'Group')], verbose_name='Chat type')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'ordering': ['-last_message__created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('msg_type', models.PositiveSmallIntegerField(choices=[(1, 'Text'), (2, 'Images'), (3, 'Files')], verbose_name='Message type')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('viewed', models.BooleanField(default=False, verbose_name='Viewed')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messenger.chat', verbose_name='Chat')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='text', serialize=False, to='messenger.message', verbose_name='Message')),
                ('content', models.TextField(verbose_name='Text content')),
            ],
            options={
                'verbose_name': 'Text Message',
                'verbose_name_plural': 'Text Messages',
                'ordering': ['message'],
            },
        ),
        migrations.CreateModel(
            name='ImageMessage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.ImageField(upload_to=messenger.utilities.get_image_message_path, verbose_name='Image content')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='messenger.message', verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Image Message',
                'verbose_name_plural': 'Image Messages',
                'ordering': ['message'],
            },
        ),
        migrations.CreateModel(
            name='FileMessage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.FileField(upload_to=messenger.utilities.get_file_message_path, verbose_name='File content')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='messenger.message', verbose_name='Message')),
            ],
            options={
                'verbose_name': 'File Message',
                'verbose_name_plural': 'File Messages',
                'ordering': ['message'],
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message', to='messenger.message', verbose_name='Last message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Members'),
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('chat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='group_details', serialize=False, to='messenger.chat', verbose_name='Chat')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('image', models.ImageField(blank=True, help_text='Upload JPG or PNG image. Required minimum of size 500 x 500.', null=True, upload_to=messenger.utilities.get_chat_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png')), main.validators.MinimumImageSizeValidator(500, 500)], verbose_name='Image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Group Chat',
                'verbose_name_plural': 'Group Chats',
                'ordering': ['chat'],
            },
        ),
    ]
