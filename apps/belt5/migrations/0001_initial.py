# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 05:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='poke',
            name='by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poker', to='belt5.User'),
        ),
        migrations.AddField(
            model_name='poke',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poked', to='belt5.User'),
        ),
    ]
