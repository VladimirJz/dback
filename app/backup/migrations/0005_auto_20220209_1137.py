# Generated by Django 2.2 on 2022-02-09 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backup', '0004_auto_20220209_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backups',
            name='Comments',
            field=models.TextField(blank=True, help_text='Comments', null=True),
        ),
    ]