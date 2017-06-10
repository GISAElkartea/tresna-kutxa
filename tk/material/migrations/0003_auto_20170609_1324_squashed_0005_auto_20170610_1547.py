# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import tk.material.fields
import tk.material.models


class Migration(migrations.Migration):

    replaces = [('material', '0003_auto_20170609_1324'), ('material', '0004_auto_20170610_1450'), ('material', '0005_auto_20170610_1547')]

    dependencies = [
        ('material', '0002_auto_20170608_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='notes',
            field=tk.material.fields.AnyLocalizedField(blank=True, required=[], uniqueness=[], verbose_name='notes'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='groupfeature',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='material',
            name='brief',
            field=tk.material.fields.AnyLocalizedMarkdownxField(blank=True, required=[], uniqueness=[], verbose_name='brief'),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=tk.material.fields.AnyLocalizedField(blank=True, max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='groupfeature',
            name='name',
            field=tk.material.fields.AnyLocalizedField(blank=True, max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=tk.material.fields.AnyLocalizedField(blank=True, max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=tk.material.fields.AnyLocalizedField(blank=True, max_length=512, required=[], uniqueness=[], verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=tk.material.fields.AnyLocalizedField(blank=True, max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='video',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[tk.material.models.validate_year], verbose_name='year'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='groupfeature',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
        migrations.AlterField(
            model_name='material',
            name='slug',
            field=tk.material.fields.AnyLocalizedUniqueSlugField(include_time=False, populate_from='title', required=[], uniqueness=['eu', 'es']),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=tk.material.fields.AnyLocalizedField(max_length=512, required=[], uniqueness=[], verbose_name='izena'),
        ),
    ]
