# Generated by Django 3.2.9 on 2022-12-25 07:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.validators
import messenger.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convo_type', models.PositiveSmallIntegerField(choices=[(1, 'Dialog'), (2, 'Group')], verbose_name='Conversation type')),
                ('members', models.ManyToManyField(related_name='conversations', to=settings.AUTH_USER_MODEL, verbose_name='Members')),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.PositiveSmallIntegerField(choices=[(1, 'Text'), (2, 'Images'), (3, 'Files')], verbose_name='Message type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_viewed', models.BooleanField(default=False, verbose_name='Viewed')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messenger.conversation', verbose_name='Conversation')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['created_at', 'id'],
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to=messenger.utilities.get_file_message_path, verbose_name='File content')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='messenger.message', verbose_name='Message')),
            ],
            options={
                'verbose_name': 'File Message',
                'verbose_name_plural': 'File Messages',
                'ordering': ['message'],
            },
        ),
        migrations.CreateModel(
            name='GroupConversation',
            fields=[
                ('conversation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='group_details', serialize=False, to='messenger.conversation', verbose_name='Conversation')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('image', models.ImageField(blank=True, help_text='Upload JPG or PNG image. Required minimum of size 500 x 500.', null=True, upload_to=messenger.utilities.get_conversation_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png')), main.validators.MinimumImageSizeValidator(500, 500)], verbose_name='Image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Group Conversation',
                'verbose_name_plural': 'Group Conversations',
                'ordering': ['-conversation'],
            },
        ),
    ]
