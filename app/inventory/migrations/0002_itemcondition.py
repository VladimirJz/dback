# Generated by Django 2.2 on 2022-02-03 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Condition', models.CharField(help_text='Item Condition', max_length=30, verbose_name='Item condition')),
            ],
        ),
    ]