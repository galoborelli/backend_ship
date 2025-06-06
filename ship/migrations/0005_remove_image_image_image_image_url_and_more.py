# Generated by Django 4.2 on 2025-05-13 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0004_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='section',
            field=models.CharField(choices=[('hero', 'Hero'), ('how-it-works', 'How it works'), ('carrousel', 'Carrusel'), ('reserve', 'Reserve')], max_length=20),
        ),
    ]
