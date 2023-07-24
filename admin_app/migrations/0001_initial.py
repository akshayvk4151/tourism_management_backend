# Generated by Django 4.2 on 2023-05-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blog_topic', models.CharField(max_length=200)),
                ('post_date', models.DateField()),
                ('blog_description', models.CharField(max_length=800)),
                ('blog_image', models.ImageField(upload_to='blog/')),
            ],
            options={
                'db_table': 'blog_tb',
            },
        ),
    ]