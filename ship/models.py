from django.db import models




class Schedules(models.Model):
    TIPO_HORARIO = [
        ('mañana', 'Mañana (8:00 a 12:00)'),
        ('mañana', 'Mañana (9:00 a 13:00)'),
        ('mañana', 'Mañana (10:00 a 14:00)'),
        ('tarde', 'Tarde (13:00 a 19:00)'),
        ('tarde', 'Tarde (14:00 a 20:00)'),
        ('tarde', 'Tarde (14:00 a 18:00)'),
        ('tarde', 'Tarde (15:00 a 19:00)'),
        ('tarde', 'Tarde (16:00 a 20:00)'),
        
    ]

    type = models.CharField(max_length=10, choices=TIPO_HORARIO)
    init_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.init_hour} a {self.end_hour }"



class Reserve(models.Model):
    id_reserve = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField("Email o Teléfono", max_length=100)
    date_selected = models.DateField()
    time_selected = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.date_selected} {self.time_selected}"





SECTION_CHOICES = [
    ('hero', 'hero'),
    ('how-it-works', 'how it works'),
    ('carrousel', 'carrusel'),
    ('reserve', 'reserve'),
]

class Image(models.Model):
    title = models.CharField(max_length=100)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    image_url = models.URLField(max_length=200)  
    order = models.PositiveIntegerField(default=0)  # Para orden personalizado

    def __str__(self):
        return f"{self.section} - {self.title} {self.image_url}"

    # Este método extra es útil para que el admin de Django lo muestre bien
    def image(self):
        return self.image_url
