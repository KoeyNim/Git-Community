# Generated by Django 3.1.7 on 2021-04-26 05:36

from django.db import migrations, models
import login.Validators


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210422_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=11, validators=[login.Validators.PhoneValidate], verbose_name='전화번호'),
        ),
    ]
