# Generated by Django 2.2.4 on 2019-09-22 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quanlitaisan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taisan',
            old_name='thoi_han_bh',
            new_name='thoi_han_bao_hanh',
        ),
    ]
