# Generated by Django 4.2 on 2023-05-18 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_customer_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.BigIntegerField()),
                ('email', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'contact_tb',
            },
        ),
    ]
