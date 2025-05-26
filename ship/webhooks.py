import os
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Reserve
from django.core.mail import send_mail

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
        name = session.get('metadata', {}).get('name')
        contact = session.get('metadata', {}).get('contact')
        date_selected = session.get('metadata', {}).get('date_selected')
        time_selected = session.get('metadata', {}).get('time_selected')
        quantity = session.get('metadata', {}).get('quantity')
        message = session.get('metadata', {}).get('message')
        status = 'confirmed'
        print(f"Checkout completado para reserva {id_reserve}")

        reserve, created = Reserve.objects.get_or_create(id=id_reserve)
        reserve.name = name
        reserve.contact = contact
        reserve.date_selected = date_selected
        reserve.time_selected = time_selected
        reserve.quantity = quantity
        reserve.message = message
        reserve.status = status
        reserve.save()

        send_mail(
            'Reserva confirmada',
            f'Hola {name}, tu reserva para {date_selected} a las {time_selected} ha sido confirmada.',
            'tuemail@dominio.com',
            [contact],
            fail_silently=True,
        )
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        id_reserve = metadata.get('id_reserve')

        try:
            reserve = Reserve.objects.get(id=id_reserve)
            reserve.status = 'cancelled'
            reserve.save()
        except Reserve.DoesNotExist:
            pass  # Podés loguearlo o ignorarlo
    return HttpResponse(status=200)
