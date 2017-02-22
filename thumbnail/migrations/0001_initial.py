# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hexdigest', models.CharField(max_length=32, db_index=True)),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to=b'thumbnails')),
            ],
        ),
    ]
