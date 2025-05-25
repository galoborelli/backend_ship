import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Reserve
from django.conf import settings
from django.core.mail import send_mail

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        # Evitar duplicados: por ejemplo usando id_reserve único y crear reserva si no existe
        id_reserve = metadata.get('id_reserve')

        if id_reserve and not Reserve.objects.filter(id_reserve=id_reserve).exists():
            Reserve.objects.create(
                id_reserve=id_reserve,
                name=metadata.get('name', ''),
                contact=metadata.get('contact', ''),
                date_selected=metadata.get('date_selected', ''),
                time_selected=metadata.get('time_selected', ''),
                quantity=metadata.get('quantity', 1),
                message=metadata.get('message', ''),
            )
            

        # Mandar email al cliente
    send_mail(
        'Confirmación de tu reserva',
        f'Hola {metadata.get("name")}, tu reserva para el día {metadata.get("date_selected")} a las {metadata.get("time_selected")} fue confirmada. ¡Gracias!',
        'no-reply@tu-dominio.com',
        [metadata.get('contact')],
        fail_silently=False,
    )

    return HttpResponse(status=200)
