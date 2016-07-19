# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hits',
            fields=[
                ('hits_id', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('periodLS', models.FloatField(default=0.0)),
                ('period_fit', models.FloatField(default=0.0)),
                ('mag_mean', models.FloatField(default=0.0)),
                ('mag_std', models.FloatField(default=0.0)),
                ('true_label', models.CharField(max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HitsDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mjd', models.FloatField(default=0.0)),
                ('mag', models.FloatField(default=0.0)),
                ('err', models.FloatField(default=0.0)),
                ('hits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hits.Hits')),
            ],
        ),
        migrations.CreateModel(
            name='SaveHits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Expert')),
                ('hits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hits.Hits')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='savehits',
            unique_together=set([('expert', 'hits')]),
        ),
    ]
