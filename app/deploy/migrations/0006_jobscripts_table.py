# Generated by Django 2.2 on 2022-01-24 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20220111_1046'),
        ('deploy', '0005_auto_20220123_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobscripts',
            name='Table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Tables'),
        ),
    ]
