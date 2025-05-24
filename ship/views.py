from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers  
from .models import Reserve, Schedules, Image
from .serializer import ReserveSerializer, ScheduleSerializer, ImageSerializer 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta



class ReserveListCreateAPIView(APIView):
    @swagger_auto_schema(responses={200: ReserveSerializer(many=True)})
    def get(self, request):
        reserves = Reserve.objects.all()
        serializer = ReserveSerializer(reserves, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ReserveSerializer)
    def post(self, request):
        serializer = ReserveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ReserveAvailabilityAPIView(APIView):
    @swagger_auto_schema(responses={200: ScheduleSerializer(many=True)})
    def get(self, *args, **kwargs):
        try:
            # 1. Parsear la fecha desde la URL
            fecha_reserva = kwargs['date']
            fecha_reserva_obj = datetime.fromisoformat(fecha_reserva).date()

            # 2. Obtener las reservas del día con sus horarios
            reservas_del_dia = Reserve.objects.filter(date_selected=fecha_reserva_obj).select_related('time_selected')
            horarios_reservados = [
                (reserva.time_selected.init_hour, reserva.time_selected.end_hour)
                for reserva in reservas_del_dia
            ]

            # 3. Traer todos los horarios posibles
            todos_los_horarios = Schedules.objects.all()

            horarios_disponibles = []

            # 4. Verificamos si cada horario tiene al menos 2 horas de separación
            for horario in todos_los_horarios:
                disponible = True
                for init_res, end_res in horarios_reservados:
                    if not (
                        horario.init_hour >= (datetime.combine(fecha_reserva_obj, end_res) + timedelta(hours=2)).time()
                        or horario.end_hour <= (datetime.combine(fecha_reserva_obj, init_res) - timedelta(hours=2)).time()
                    ):
                        disponible = False
                        break
                if disponible:
                    horarios_disponibles.append(horario)

            serializer = ScheduleSerializer(horarios_disponibles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            


class ReserveDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: ReserveSerializer()})
    def get(self, request, id):
        try:
            reserve = Reserve.objects.get(id_reserve=id)
            serializer = ReserveSerializer(reserve)
            return Response(serializer.data)
        except Reserve.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=404)

    @swagger_auto_schema(request_body=ReserveSerializer)
    def put(self, request, id):
        try:
            reserve = Reserve.objects.get(id_reserve=id)
        except Reserve.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=404)

        serializer = ReserveSerializer(reserve, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        try:
            reserve = Reserve.objects.get(id_reserve=id)
            reserve.delete()
            return Response({'message': 'Reserva eliminada'})
        except Reserve.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=404)





class GetImages(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Success', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'section': openapi.Schema(type=openapi.TYPE_STRING),
            'image_url': openapi.Schema(type=openapi.TYPE_STRING),
            'order': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))})

    def get(self, request, section):
        # Reutilizar solo la validación de sección
        try:
            validated_section = ImageSerializer().validate_section(section)
        except serializers.ValidationError as e:
            return Response({'error': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar imágenes
        images = Image.objects.filter(section=validated_section).order_by('order')
        serializer = ImageSerializer(images, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request):
        try:
            image = Image.objects.all()
            serializer = ImageSerializer(image,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

