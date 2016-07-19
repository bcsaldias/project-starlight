# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hits', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteHits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('QSO', 'Quasar'), ('CEP', 'Cepheid'), ('CV', 'Cataclysmic Variable'), ('NV', 'Non-variable'), ('RRLYR', 'RR Lyrae'), ('EB', 'Eclipsing Binary'), ('SNe', 'Supernovae')], max_length=8, null=True)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Expert')),
                ('hits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hits.Hits')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='votehits',
            unique_together=set([('expert', 'hits')]),
        ),
    ]