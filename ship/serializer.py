from rest_framework import serializers
from .models import Reserve, Schedules
import datetime, re

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'
    def validate_email(self, email):
    # Validar formato de email con expresión regular
     email_regex = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"
     if not re.match(email_regex, email):
        raise serializers.ValidationError("Formato de email inválido.")
     return email

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name
    
    def validate_date(self,dateSelected):
        today = datetime.date.today()
        if(dateSelected < today):
            raise serializers.ValidationError("La fecha no puede ser anterior a la fecha actual.")
        return date

    def validate_phone(self, phone):
        # Elimina espacios y guiones
        phoneReplace = phone.replace(" ", "").replace("-", "")

        # Validación por regex: acepta números con opcional +, código país y de 8 a 15 dígitos
        pattern = r'^(\+?\d{1,4})?\d{8,15}$'
        if not re.match(pattern, phoneReplace):
            raise serializers.ValidationError(
                "Número de teléfono inválido. Debe contener solo números, puede incluir '+' al inicio y tener entre 8 y 15 dígitos."
            )

        return phone

    def validate_cuantity(self, cuantity):
        if cuantity < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return cuantity

    def validate_time_date(self,time_date):
        # Validar que haya una hora seleccionada
        if time_date is None:
            raise serializers.ValidationError("Se debe seleccionar una hora.")
        return time_date


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
