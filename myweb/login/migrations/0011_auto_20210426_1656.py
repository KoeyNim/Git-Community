# Generated by Django 3.1.7 on 2021-04-26 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_remove_socialuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.user'),
        ),
    ]
