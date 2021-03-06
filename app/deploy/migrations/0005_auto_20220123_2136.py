# Generated by Django 2.2 on 2022-01-23 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0004_jobscripts_phase'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobs',
            options={'verbose_name_plural': 'jobs'},
        ),
        migrations.AlterModelOptions(
            name='jobscripts',
            options={'verbose_name_plural': 'scripts'},
        ),
        migrations.AlterModelOptions(
            name='tablefilters',
            options={'verbose_name_plural': 'table filters'},
        ),
        migrations.AddField(
            model_name='jobs',
            name='DestinationPath',
            field=models.CharField(blank=True, help_text='Folder Destination', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='FieldSeparator',
            field=models.CharField(blank=True, help_text='Separator', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='FilePerTable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='Type',
            field=models.SmallIntegerField(choices=[(1, 'Database deploy'), (2, 'Data Dump')], default=1, help_text='Job Type'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='SourceDB',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.DataBases'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='TargetDB',
            field=models.CharField(blank=True, help_text='Destination Database', max_length=50),
        ),
    ]
