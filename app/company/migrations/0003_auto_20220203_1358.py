# Generated by Django 2.2 on 2022-02-03 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20220203_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employ',
            name='FirstName',
        ),
        migrations.AddField(
            model_name='employ',
            name='DisplayName',
            field=models.CharField(blank=True, default='', help_text='Firstname', max_length=200),
        ),
        migrations.AlterField(
            model_name='employ',
            name='JobTittle',
            field=models.CharField(blank=True, help_text='Job tittle', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employ',
            name='LastName',
            field=models.CharField(blank=True, default='', help_text='LastName', max_length=200),
        ),
        migrations.AlterField(
            model_name='employ',
            name='Name',
            field=models.CharField(help_text='Name', max_length=200),
        ),
        migrations.AlterField(
            model_name='employ',
            name='PersonalEmail',
            field=models.EmailField(blank=True, max_length=30, null=True, verbose_name='Personal Email'),
        ),
    ]