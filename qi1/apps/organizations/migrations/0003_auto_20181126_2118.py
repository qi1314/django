# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_courseorg_catgory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='click_name',
            new_name='click_nums',
        ),
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='\u8bfe\u7a0b\u6570'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='student',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u4eba\u6570'),
        ),
    ]
