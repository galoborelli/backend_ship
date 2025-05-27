import os
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Reserve
from django.core.mail import send_mail
from .models import Schedules

# Cargar la clave secreta y webhook directamente del entorno
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    print("Stripe webhook secret cargado:", endpoint_secret)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Payload inválido:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Firma inválida:", e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        id_reserve = session.get('metadata', {}).get('id_reserve')

        if id_reserve:
            try:
                reserve = Reserve.objects.get(id=id_reserve)
                reserve.status = 'confirmed'
                reserve.save()

                send_mail(
                    'Reserva confirmada',
                    f'Hola {reserve.name}, tu reserva para {reserve.date_selected} a las {reserve.time_selected} ha sido confirmada.',
                    'tuemail@dominio.com',
                    [reserve.contact],
                    fail_silently=True,
                )
            except Reserve.DoesNotExist:
                print("Reserva no encontrada para confirmar")

    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        id_reserve = session.get('metadata', {}).get('id_reserve')

        if id_reserve:
            try:
                reserve = Reserve.objects.get(id=id_reserve)
                reserve.status = 'cancelled'
                reserve.save()
            except Reserve.DoesNotExist:
                print("Reserva no encontrada para cancelar")

    return HttpResponse(status=200)

