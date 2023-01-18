# Generated by Django 3.2.9 on 2023-01-18 17:56

import accounts.utilities
from decimal import Decimal
from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.utilities
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MWUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='Username')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email address already exists.'}, max_length=254, unique=True, verbose_name='Email address')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Administrator'), (2, 'Customer'), (3, 'Organizer')], verbose_name='User type')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('avatar', models.ImageField(blank=True, help_text='Upload JPG or PNG image. Required minimum of size 500 x 500.', null=True, upload_to=accounts.utilities.get_avatar_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png')), main.validators.MinimumImageSizeValidator(500, 500)], verbose_name='Avatar')),
                ('phone', models.CharField(blank=True, max_length=21, validators=[django.core.validators.RegexValidator(message='Wrong format!', regex='^(\\s*)?(\\+)?([- _():=+]?\\d[- _():=+]?){9,16}(\\s*)?$')], verbose_name='Phone')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.city', verbose_name='City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.country', verbose_name='Country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='OrganizerRole',
            fields=[
                ('role_id', models.PositiveSmallIntegerField(choices=[(None, '(Unknown)'), (1, 'Photographer'), (2, 'Videographer'), (3, 'Leading'), (4, 'Musician'), (5, 'DJ'), (6, 'Agency'), (7, 'Salon'), (8, 'Confectionery'), (9, 'Decorator'), (10, 'Visagiste'), (11, 'Hairdresser')], primary_key=True, serialize=False, verbose_name='Identifier')),
            ],
            options={
                'verbose_name': 'Role of Organizer',
                'verbose_name_plural': 'Roles of Organizers',
                'ordering': ['role_id'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='customer', serialize=False, to='accounts.mwuser', verbose_name='User')),
                ('date_of_wedding', models.DateField(blank=True, null=True, verbose_name='Date of Wedding')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='organizer', serialize=False, to='accounts.mwuser', verbose_name='User')),
                ('cover', models.ImageField(blank=True, help_text='Upload JPG or PNG image. Required minimum of size 1500 x 500.', null=True, upload_to=main.utilities.get_cover_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png')), main.validators.MinimumImageSizeValidator(1500, 500)], verbose_name='Cover')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('cost_work', models.DecimalField(decimal_places=2, default=0.0, help_text='Please enter in USD ($)', max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Cost of work')),
                ('number_hours', models.PositiveIntegerField(default=0, verbose_name='Number of hours')),
                ('profile_url', models.SlugField(max_length=64, unique=True, verbose_name='Profile URL')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=2, verbose_name='Rating')),
                ('pro_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Pro-account valid time')),
                ('cities', models.ManyToManyField(blank=True, to='main.City', verbose_name='Cities')),
                ('countries', models.ManyToManyField(blank=True, to='main.Country', verbose_name='Countries')),
                ('languages', models.ManyToManyField(blank=True, to='main.Language', verbose_name='Languages')),
                ('roles', models.ManyToManyField(blank=True, to='accounts.OrganizerRole', verbose_name='Roles')),
            ],
            options={
                'verbose_name': 'Organizer',
                'verbose_name_plural': 'Organizers',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='ConnectionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=64, verbose_name='Device ID')),
                ('online', models.BooleanField(default=False, verbose_name='Online')),
                ('first_login', models.DateTimeField(auto_now_add=True, verbose_name='First login')),
                ('last_visit', models.DateTimeField(auto_now=True, verbose_name='Last visit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_histories', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Connection History',
                'verbose_name_plural': 'Connection Histories',
                'ordering': ['user', '-last_visit'],
            },
        ),
        migrations.CreateModel(
            name='OrganizerLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_type', models.CharField(choices=[('WE', 'Website'), ('FK', 'Facebook'), ('TR', 'Twitter'), ('IM', 'Instagram'), ('SY', 'Spotify'), ('YE', 'YouTube'), ('SD', 'SoundCloud'), ('PT', 'Pinterest'), ('VK', 'VK'), ('LN', 'LinkedIn')], default='WE', max_length=2, verbose_name='Type of Link')),
                ('link_url', models.URLField(verbose_name='URL of Link')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizer_links', to='accounts.organizer', verbose_name='Organizer')),
            ],
            options={
                'verbose_name': 'Link of Organizer',
                'verbose_name_plural': 'Links of Organizer',
                'ordering': ['organizer', 'id'],
            },
        ),
        migrations.AddConstraint(
            model_name='connectionhistory',
            constraint=models.UniqueConstraint(fields=('user', 'device_id'), name='unique_connectionhistory'),
        ),
    ]
