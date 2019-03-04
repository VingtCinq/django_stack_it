# Generated by Django 2.1.5 on 2019-01-18 08:41

from django.db import migrations, models
import stack_it.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('stack_it', '0009_auto_20190117_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepagecontent',
            name='size',
            field=models.CharField(default='800x600', max_length=50, validators=[stack_it.utils.validators.validate_image_size], verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='modelpagecontent',
            name='model_name',
            field=models.CharField(max_length=50, validators=[stack_it.utils.validators.validate_model_name], verbose_name='Model Name'),
        ),
    ]
