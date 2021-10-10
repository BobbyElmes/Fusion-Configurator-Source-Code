# Generated by Django 3.1 on 2021-06-07 00:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('SessionId', models.AutoField(primary_key=True, serialize=False)),
                ('IpAddress', models.CharField(max_length=50)),
                ('QueryId', models.CharField(max_length=20)),
                ('FirstAccessed', models.DateTimeField(default=datetime.datetime.now)),
                ('LastAccessed', models.DateTimeField(default=datetime.datetime.now)),
                ('AddQuoteNum', models.IntegerField(default=0)),
                ('PDFNum', models.IntegerField(default=0)),
                ('XLSXNum', models.IntegerField(default=0)),
                ('Mobile', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QueryId_CompanyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QueryId', models.CharField(max_length=20)),
                ('CompanyName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=35, unique=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
