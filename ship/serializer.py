from rest_framework import serializers
from .models import Reserve, Schedules, Image
import datetime, re

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'


    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name
    
    def validate_date(self,dateSelected):
        today = datetime.date.today()
        if(dateSelected < today):
            raise serializers.ValidationError("La fecha no puede ser anterior a la fecha actual.")
        return date
    def validate_contact(self, value):
        # Regex para email
        email_regex = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"
        # Regex para teléfono internacional (con o sin +)
        phone_regex = r'^(\+?\d{1,4})?\d{8,15}$'
        
        # Limpia espacios o guiones del número de teléfono
        clean_value = value.replace(" ", "").replace("-", "")

        if re.match(email_regex, value):
            return value  # Es un email válido
        elif re.match(phone_regex, clean_value):
            return clean_value  # Es un teléfono válido (sin espacios/guiones)
        else:
            raise serializers.ValidationError(
                "Debe ingresar un email válido o un número de teléfono válido."
            )
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



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
    def validate_section(self, section):
        # Validar que la sección esté en las opciones definidas
        valid_sections = ['hero', 'how-it-works', 'carrousel', 'reserve']
        if section not in valid_sections:
            raise serializers.ValidationError(f"Sección inválida. Debe ser una de: {', '.join(valid_sections)}.")
        return section
    
    
    