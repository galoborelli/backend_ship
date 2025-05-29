from django.db import models




class Schedules(models.Model):
    TIPO_HORARIO = [
        ('mañana_1', 'Mañana (8:00 a 12:00)'),
        ('mañana_2', 'Mañana (9:00 a 13:00)'),
        ('mañana_3', 'Mañana (10:00 a 14:00)'),
        ('tarde_1', 'Tarde (13:00 a 19:00)'),
        ('tarde_2', 'Tarde (14:00 a 20:00)'),
        ('tarde_3', 'Tarde (14:00 a 18:00)'),
        ('tarde_4', 'Tarde (15:00 a 19:00)'),
        ('tarde_5', 'Tarde (16:00 a 20:00)'),
    ]

    type = models.CharField(max_length=10, choices=TIPO_HORARIO)
    init_hour = models.TimeField()
    end_hour = models.TimeField()

def __str__(self):
    return f"{self.get_type_display()} - {self.init_hour.strftime('%H:%M')} a {self.end_hour.strftime('%H:%M')}"



class Reserve(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
    ]


    id_reserve = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField("Email o Teléfono", max_length=100)
    date_selected = models.DateField()
    time_selected = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # method_payment = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')
    
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
