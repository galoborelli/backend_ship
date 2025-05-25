from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers  
from .models import Reserve, Schedules, Image
from .serializer import ReserveSerializer, ScheduleSerializer, ImageSerializer 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
import stripe
from django.conf import settings

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


class CreateCheckoutSessionView(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Success', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))})
    def post(self, request):
        data = request.data
        print("Datos recibidos para checkout:", data)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(data['amount']) * 100,  # precio en centavos
                        'product_data': {
                            'name': 'Reserva de turno',
                        },
                    },
                    'quantity': 1,
                }],
                metadata={
                    'id_reserve': data['id_reserve'],
                    'name': data['name'],
                    'contact': data['contact'],
                    'date_selected': data['date_selected'],
                    'time_selected': data['time_selected'],
                    'quantity': data['quantity'],
                    'message': data['message'],
                },
                success_url='https://frontend-ship-blond.vercel.app/success',
                cancel_url='https://frontend-ship-blond.vercel.app/cancel',
            )
            print(f"Checkout session creada con id: {checkout_session.id}")
            return Response({'checkout_url': checkout_session.url})
        except Exception as e:
            print(f"Error creando checkout session: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ReserveAvailabilityAPIView(APIView):
    @swagger_auto_schema(responses={200: ScheduleSerializer(many=True)})
    def get(self, *args, **kwargs):
        try:
            fecha_reserva = kwargs['date']
            fecha_reserva_obj = datetime.fromisoformat(fecha_reserva).date()

            # Todas las reservas para esa fecha
            reservas_del_dia = Reserve.objects.filter(date_selected=fecha_reserva_obj)
            todos_los_horarios = Schedules.objects.all()

            # Lista de horarios reservados
            horarios_reservados = [
                {
                    'init': datetime.combine(fecha_reserva_obj, reserva.time_selected.init_hour),
                    'end': datetime.combine(fecha_reserva_obj, reserva.time_selected.end_hour)
                }
                for reserva in reservas_del_dia
            ]

            horarios_disponibles = []
            for horario in todos_los_horarios:
                horario_inicio = datetime.combine(fecha_reserva_obj, horario.init_hour)
                horario_fin = datetime.combine(fecha_reserva_obj, horario.end_hour)

                es_valido = True
                for reservado in horarios_reservados:
                    # Si la diferencia entre el inicio del horario y el fin de uno reservado es < 2hs
                    diferencia_inicio = abs((horario_inicio - reservado['end']).total_seconds()) / 3600
                    diferencia_fin = abs((horario_fin - reservado['init']).total_seconds()) / 3600

                    if (reservado['end'] > horario_inicio and reservado['init'] < horario_fin) or \
                       diferencia_inicio < 2 or diferencia_fin < 2:
                        es_valido = False
                        break

                if es_valido:
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
    

