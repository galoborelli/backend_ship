from django.urls import path
from .views import ReserveListCreateAPIView, ReserveDetailAPIView, ReserveAvailabilityAPIView, GetImages, CreateCheckoutSessionView
from .webhooks import stripe_webhook

urlpatterns = [
    path('reserves/', ReserveListCreateAPIView.as_view(), name='reserves'),
    path('reserves/<int:id>/', ReserveDetailAPIView.as_view(), name='reserve-detail'),
    path('reserves/<str:date>/',ReserveAvailabilityAPIView.as_view(), name='reserve-availability'),
    path('reserves/checkout/', CreateCheckoutSessionView.as_view(), name='create_checkout'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
    path('images/', GetImages.as_view(), name='image'),
]
