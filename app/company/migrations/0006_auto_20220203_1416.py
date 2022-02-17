# Generated by Django 2.2 on 2022-02-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20220203_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employ',
            name='CURP',
            field=models.CharField(blank=True, default='', help_text='CURP', max_length=18),
        ),
        migrations.AlterField(
            model_name='employ',
            name='RFC',
            field=models.CharField(blank=True, default='', help_text='RFC', max_length=13),
        ),
    ]