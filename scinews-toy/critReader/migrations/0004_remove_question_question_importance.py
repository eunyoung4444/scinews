# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-11 17:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('critReader', '0003_remove_question_question_cueword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_importance',
        ),
    ]
