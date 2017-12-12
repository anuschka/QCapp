# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-12 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qcapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('type', models.CharField(max_length=100)),
                ('lot', models.CharField(max_length=100)),
                ('expiry', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CellPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('lot', models.CharField(max_length=100)),
                ('expiry', models.DateTimeField(null=True)),
                ('sheet', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'P', b'PK'), (b'N', b'NK')], max_length=1)),
                ('result', models.IntegerField(choices=[(0, b'0'), (1, b'+1'), (2, b'+2'), (3, b'+3'), (4, b'+4')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcapp.Cell')),
            ],
        ),
        migrations.CreateModel(
            name='Essey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IdCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('lot', models.CharField(max_length=100)),
                ('expiry', models.DateTimeField(null=True)),
                ('manufacturer', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reagent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('lot', models.CharField(help_text=b'Lot number', max_length=100)),
                ('expiry', models.DateField(null=True)),
                ('manufacturer', models.CharField(max_length=100)),
                ('requiresIDcard', models.BooleanField(default=False, help_text=b'Require ID card')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('roles', models.CharField(choices=[(b'T', b'Technician'), (b'D', b'Doctor'), (b'A', b'Admin')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(max_length=200, null=True)),
                ('consequence', models.CharField(choices=[(b'P', b'OK'), (b'N', b'NOT OK')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('essey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='essey_validation', to='qcapp.Essey')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technician', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SimpleItem',
        ),
        migrations.AlterUniqueTogether(
            name='reagent',
            unique_together=set([('type', 'manufacturer', 'lot')]),
        ),
        migrations.AlterUniqueTogether(
            name='idcard',
            unique_together=set([('type', 'manufacturer', 'lot')]),
        ),
        migrations.AddField(
            model_name='essey',
            name='idcard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idcard_essey', to='qcapp.IdCard'),
        ),
        migrations.AddField(
            model_name='essey',
            name='reagent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reagent_essey', to='qcapp.Reagent'),
        ),
        migrations.AddField(
            model_name='control',
            name='essey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='essey_control', to='qcapp.Essey'),
        ),
        migrations.AlterUniqueTogether(
            name='cellpanel',
            unique_together=set([('type', 'manufacturer', 'lot')]),
        ),
        migrations.AddField(
            model_name='cell',
            name='cell_panel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcapp.CellPanel'),
        ),
        migrations.AlterUniqueTogether(
            name='essey',
            unique_together=set([('type', 'created_at')]),
        ),
        migrations.AlterUniqueTogether(
            name='cell',
            unique_together=set([('number', 'cell_panel')]),
        ),
    ]
