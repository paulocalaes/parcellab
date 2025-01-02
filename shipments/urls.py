from django.urls import path
from .views.shipment_list import ShipmentList
from .views.shipment_tracking import ShipmentTracking
from .views.shipment_carrier import ShipmentCarrier
from .views.shipment_detail import ShipmentDetail

urlpatterns = [
    path('', ShipmentList.as_view(), name='shipment-list'),
    path('<int:shipment_id>', ShipmentDetail.as_view(), name='shipment-detail'),
    path('tracking/<str:tracking_number>', ShipmentTracking.as_view(), name='shipment-tracking'),
    path('carrier/<str:carrier>', ShipmentCarrier.as_view(), name='shipment-carrier'),
    
]