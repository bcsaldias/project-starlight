# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('macho', '0006_machodetail_err'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveMACHO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Expert')),
                ('macho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macho.Macho')),
            ],
        ),
    ]
