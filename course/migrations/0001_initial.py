# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import course.models
import tinymce.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('short', models.CharField(max_length=30, null=True, blank=True)),
                ('position', models.CharField(max_length=150, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=course.models.get_file_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100, null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=course.models.get_file_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book_date', models.DateTimeField(auto_now_add=True)),
                ('train_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
                ('icon', models.CharField(max_length=30, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField(null=True, blank=True)),
                ('price', models.FloatField(default=0)),
                ('hours', models.IntegerField(default=0)),
                ('lessons', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=0)),
                ('level', models.CharField(default=b'B', max_length=1, choices=[(b'B', b'Basic'), (b'M', b'Medium'), (b'A', b'Advance')])),
                ('is_hot', models.BooleanField(default=False)),
                ('is_publish', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(null=True, upload_to=course.models.get_file_path, blank=True)),
                ('accounts', models.ManyToManyField(to='course.Account', blank=True)),
                ('authors', models.ManyToManyField(to='course.Author')),
                ('category', models.ForeignKey(to='course.Category')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=150)),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('website', models.URLField(max_length=150, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(unique=True, max_length=150)),
                ('phone', models.CharField(max_length=30)),
                ('org', models.CharField(max_length=200, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transfer_via', models.CharField(max_length=1, choices=[(b'E', b'Email'), (b'P', b'Phone'), (b'M', b'Mail'), (b'F', b'Fax'), (b'S', b'SMS'), (b'L', b'Line'), (b'D', b'Direct')])),
                ('transfer_date', models.DateField(null=True, blank=True)),
                ('transfer_amount', models.FloatField(default=0)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('reg_status', models.CharField(default=b'R', max_length=1, choices=[(b'R', b'Register'), (b'P', b'Paid'), (b'T', b'Partial'), (b'C', b'Cancel')])),
                ('member', models.ForeignKey(to='course.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('start', models.DateField(null=True, blank=True)),
                ('finish', models.DateField(null=True, blank=True)),
                ('open_date', models.CharField(max_length=50, null=True, blank=True)),
                ('total_hour', models.IntegerField(default=0)),
                ('time', models.CharField(max_length=30, null=True, blank=True)),
                ('min_people', models.IntegerField(default=0)),
                ('max_people', models.IntegerField(default=0)),
                ('promotion', models.CharField(max_length=100, null=True, blank=True)),
                ('discount', models.FloatField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('sale_price', models.FloatField(default=0)),
                ('is_publish', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='course.Course')),
                ('location', models.ForeignKey(blank=True, to='course.Location', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='register',
            name='trainging',
            field=models.ForeignKey(to='course.Training'),
        ),
        migrations.AddField(
            model_name='booking',
            name='course',
            field=models.ForeignKey(to='course.Course'),
        ),
        migrations.AddField(
            model_name='booking',
            name='member',
            field=models.ForeignKey(to='course.Member'),
        ),
        migrations.AddField(
            model_name='account',
            name='bank',
            field=models.ForeignKey(blank=True, to='course.Bank', null=True),
        ),
    ]
