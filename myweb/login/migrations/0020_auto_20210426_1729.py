# Generated by Django 3.1.7 on 2021-04-26 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_remove_socialuser_name2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialuser',
            old_name='name',
            new_name='user',
        ),
    ]
