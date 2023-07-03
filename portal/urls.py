from django.urls import path
from .views import *

urlpatterns = [
    path('', MyShipment.as_view(),name="home"),
    path('login/', Login.as_view(),name="login"),
    path('sign-up/',SignUp.as_view(), name="sign_up"),
    path('logout/',Logout.as_view(), name="logout"),
    path('search-freight-rates/',SearchFreightRates.as_view(), name="search_freight_rates"),
    path('book-shipping-containers/',BookShippingContainers.as_view(), name="book_shipping_containers"),
    path('my-shipment/',MyShipment.as_view(), name="my_shipment"),
    path('get-booked-container/',getBookedContainerList,name="get_booked_cont"),
    path('get-service-charge/',getServiceChargeView,name="get_service_charge"),
    path('get-cont-charge/',getContainerChargeView,name="get_cont_charge"),
]
