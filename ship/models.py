from django.db import models



class Schedules(models.Model):
    TIPO_HORARIO = [
        ('mañana', 'Mañana (10:00 a 14:00)'),
        ('tarde', 'Tarde (13:00 a 19:00)'),
    ]

    type = models.CharField(max_length=10, choices=TIPO_HORARIO)
    init_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.init_hour} a {self.end_hour }"



class Reserve(models.Model):
    id_reserve = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_reserve = models.DateField()
    time_reserve = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    cuantity = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.date_reserve} {self.time_reserve}"





SECTION_CHOICES = [
    ('home', 'Inicio'),
    ('services', 'Servicios'),
    ('about', 'Nosotros'),
    ('gallery', 'Galería'),
]

class Image(models.Model):
    title = models.CharField(max_length=100)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    image = models.ImageField(upload_to='images/')
    order = models.PositiveIntegerField(default=0)  # Para orden personalizado

    def __str__(self):
        return f"{self.section} - {self.title}"


