# Generated by Django 2.2.6 on 2019-10-22 08:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker', '0003_index_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerremote',
            name='whitelist_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), null=True, size=None),
        ),
    ]
