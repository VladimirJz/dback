# Generated by Django 2.2 on 2022-01-10 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20211231_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='SourceDB',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='SourceOf', to='catalog.DataBases'),
        ),
    ]