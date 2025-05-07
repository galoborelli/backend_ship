from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reserve, Schedules
from .serializer import ReserveSerializer, ScheduleSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime



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
            # Convertir el valor de la fecha a un objeto de fecha
            fecha_reserva = kwargs['date']
            fecha_reserva_obj = datetime.fromisoformat(fecha_reserva)

            # Traemos todas las reservas en esa fecha
            reservas_del_dia = Reserve.objects.filter(date_reserve=fecha_reserva_obj)
            
            # Extraemos los tipos de turnos reservados (mañana/tarde)
            tipos_reservados = reservas_del_dia.values_list('time_reserve__type', flat=True)

            # Obtenemos todos los horarios (mañana/tarde)
            todos_los_horarios = Schedules.objects.all()

            # Filtramos los horarios que NO están en tipos_reservados
            horarios_disponibles = todos_los_horarios.exclude(type__in=tipos_reservados)

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





