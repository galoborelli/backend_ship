from django.urls import path
from .views import ReserveListCreateAPIView, ReserveDetailAPIView, ReserveAvailabilityAPIView, GetImages, CreateCheckoutSessionView, CreateReservationCash, GetVideos
from .webhooks import stripe_webhook

urlpatterns = [
    path('reserves/', ReserveListCreateAPIView.as_view(), name='reserves'),
    path('reserves/<int:id>/', ReserveDetailAPIView.as_view(), name='reserve-detail'),
    path('reserves/<str:date>/',ReserveAvailabilityAPIView.as_view(), name='reserve-availability'),
    path('checkout/', CreateCheckoutSessionView.as_view(), name='create_checkout'),
    path('checkout_cash/', CreateReservationCash.as_view(), name='create_reservation_cash'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('images/', GetImages.as_view(), name='image'),
    path('videos/', GetVideos.as_view(), name='video'),
]
