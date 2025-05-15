from django.db import migrations

def fill_image_url(apps, schema_editor):
    Image = apps.get_model('ship', 'Image')
    default_url = 'https://example.com/placeholder.jpg'  # Cambiar por URL válida

    images = Image.objects.filter(image_url__isnull=True) | Image.objects.filter(image_url='')
    for img in images:
        img.image_url = default_url
        img.save()

class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0006_alter_image_image_url_alter_image_section'),  # poné la última migración aplicada
    ]

    operations = [
        migrations.RunPython(fill_image_url),
    ]