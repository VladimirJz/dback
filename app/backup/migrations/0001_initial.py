# Generated by Django 2.2 on 2022-01-17 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0005_auto_20220111_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobName', models.CharField(help_text='Backup Job name', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LocationName', models.CharField(help_text='Location name', max_length=50)),
                ('FilesPath', models.CharField(help_text='Location path', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(help_text='Status', max_length=20)),
                ('Description', models.CharField(help_text='Status description', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.SmallIntegerField(help_text='No.Rule')),
                ('Rule', models.CharField(help_text='Rule rotation name', max_length=40)),
                ('Status', models.SmallIntegerField(choices=[(1, 'Enable'), (2, 'Disable')], default=1)),
                ('RetentionDays', models.SmallIntegerField(help_text='Retention days')),
                ('FileFormat', models.CharField(help_text='Backup format', max_length=6)),
                ('Job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backup.Jobs')),
                ('Location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backup.Locations')),
            ],
        ),
        migrations.CreateModel(
            name='Backups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CreationDate', models.DateField(blank=True, help_text='Create date', null=True)),
                ('StartBackup', models.DateTimeField(blank=True, help_text='Backup start time', null=True)),
                ('EndBackup', models.DateTimeField(blank=True, help_text='Backup end time', null=True)),
                ('FileName', models.CharField(help_text='File name', max_length=100)),
                ('SizeMB', models.DecimalField(decimal_places=2, help_text='Size MB', max_digits=20)),
                ('Size', models.BigIntegerField(help_text='Size')),
                ('Comments', models.TextField(help_text='Comments')),
                ('Database', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.DataBases')),
                ('Job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backup.Jobs')),
                ('Location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backup.Locations')),
                ('Status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backup.Status')),
            ],
            options={
                'db_table': 'backup_files',
            },
        ),
    ]
