# Generated by Django 2.2 on 2022-02-03 18:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OfficeName', models.CharField(help_text='Office name', max_length=30, verbose_name='Office')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BirthDate', models.DateField(blank=True, null=True)),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Name', max_length=20)),
                ('FirstName', models.CharField(blank=True, default='', help_text='Firstname', max_length=20)),
                ('LastName', models.CharField(blank=True, default='', help_text='LastName', max_length=20)),
                ('RFC', models.CharField(blank=True, help_text='RFC', max_length=13)),
                ('CURP', models.CharField(blank=True, help_text='CURP', max_length=18)),
                ('JobTittle', models.CharField(help_text='Job tittle', max_length=50)),
                ('CompanyEmail', models.EmailField(max_length=30, verbose_name='Office Email')),
                ('PersonalEmail', models.EmailField(max_length=30, verbose_name='Personal Email')),
                ('PhoneNumber', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('Office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Office')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]