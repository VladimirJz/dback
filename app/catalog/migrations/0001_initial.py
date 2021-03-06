# Generated by Django 2.2 on 2021-11-26 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Server', models.CharField(help_text='Server name', max_length=50)),
                ('Host', models.CharField(help_text='IP or Hostname', max_length=50)),
                ('Instance', models.CharField(help_text='Instance Name', max_length=50)),
                ('Port', models.IntegerField(help_text='Port Number')),
                ('Type', models.SmallIntegerField(choices=[(1, 'MS SQLServer'), (2, 'MySQL/MariaDB'), (3, 'PostgreSQL')], default=1)),
                ('Status', models.SmallIntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Inaccessible')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TableCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(help_text='Object Bussines Category', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Schema', models.CharField(help_text='Schema Database', max_length=20, null=True)),
                ('Name', models.CharField(help_text='Database name', max_length=50)),
                ('ObjectID', models.CharField(help_text='Internal SGDB ID', max_length=50, null=True)),
                ('CreateDate', models.DateField(help_text='Creation date')),
                ('Status', models.SmallIntegerField(choices=[(1, 'Active'), (2, 'Offline'), (3, 'Deleted')], default=1)),
                ('TableCategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.TableCategory')),
            ],
        ),
        migrations.CreateModel(
            name='DataBases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Database', models.CharField(help_text='Database Name', max_length=50)),
                ('Server', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Servers')),
            ],
        ),
    ]
