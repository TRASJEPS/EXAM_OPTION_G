# Generated by Django 2.2 on 2020-12-23 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20201221_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_comment_likes',
            field=models.ManyToManyField(related_name='comment_likes', to='app1.User'),
        ),
    ]
