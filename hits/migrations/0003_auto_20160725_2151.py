# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0002_auto_20160725_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votehits',
            name='hits',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='hits.Hits'),
        ),
    ]