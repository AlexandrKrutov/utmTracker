# Generated by Django 4.1.2 on 2022-10-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utm', '0002_projectsutm_utm_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectsutm',
            name='utm_campaign',
            field=models.CharField(max_length=100, unique=True, verbose_name='utm_campaign'),
        ),
    ]