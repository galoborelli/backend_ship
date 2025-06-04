from rest_framework import serializers
from .models import Reserve, Schedules, Image, Video
import datetime, re


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['id', 'type', 'init_hour', 'end_hour']


class VideoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Video
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    init_hour = serializers.TimeField(source='time_selected.init_hour', read_only=True)
    end_hour = serializers.TimeField(source='time_selected.end_hour', read_only=True)
    
    class Meta:
        model = Reserve
        fields = '__all__'
        read_only_fields = ['status']

    def validate_name(self, name):
        if len(name.strip()) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name

    def validate_date_selected(self, date_selected):
        today = datetime.date.today()
        if date_selected < today:
            raise serializers.ValidationError("La fecha no puede ser anterior a la fecha actual.")
        return date_selected

    def validate_contact(self, value):
        email_regex = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"
        phone_regex = r'^(\+?\d{1,4})?\d{8,15}$'

        clean_value = value.replace(" ", "").replace("-", "")
        if re.match(email_regex, value):
            return value
        elif re.match(phone_regex, clean_value):
            return clean_value
        else:
            raise serializers.ValidationError(
                "Debe ingresar un email válido o un número de teléfono válido."
            )

    def validate_quantity(self, quantity):
        if quantity < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return quantity

    def validate_time_selected(self, time_selected):
        if not time_selected:
            raise serializers.ValidationError("Se debe seleccionar una hora válida.")
        return time_selected





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
    
    
    