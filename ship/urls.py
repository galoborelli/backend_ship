from django.urls import path
from .views import ReserveListCreateAPIView, ReserveDetailAPIView, ReserveAvailabilityAPIView

urlpatterns = [
    path('reserves/', ReserveListCreateAPIView.as_view(), name='reserves'),
    path('reserves/<int:id>/', ReserveDetailAPIView.as_view(), name='reserve-detail'),
    path('reserves/<str:date>/',ReserveAvailabilityAPIView.as_view(), name='reserve-availability')
]
