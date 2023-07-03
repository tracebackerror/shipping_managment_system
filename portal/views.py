from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from portal.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime

from portal.utils import getContainerCharge, getFreightRates, getIndianPortsList, getServiceCharge
from .forms import *


class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class SignUp(CreateView):
    template_name = 'sign_up.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class SearchFreightRates(TemplateView):
    template_name = 'search_freight_rates.html'
    extra_context = {}

    def get(self, *args, **kwargs):
        self.extra_context["port_list"] = getIndianPortsList()
        self.extra_context["source_port"] = "INMAA"
        self.extra_context["dest_port"] = "INVTZ"
        self.extra_context["transportation_by"] = "fcl"
        self.extra_context["container_type"] = "10std"
        self.extra_context["service_charge"] = ""
        self.extra_context["container_charge"] = ""
        self.extra_context["total"] = ""
        return super().get(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        res = getFreightRates(self.request.POST.dict())
        self.extra_context.update(self.request.POST.dict())
        self.extra_context.update(res)
        return super().get(self, *args, **kwargs)


class BookShippingContainers(LoginRequiredMixin, TemplateView):
    template_name = 'book_shipping_containers.html'
    login_url = reverse_lazy("login")
    extra_context = {}

    def get(self, *args, **kwargs):
        self.extra_context["port_list"] = getIndianPortsList()
        return super().get(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        new_order = Order()
        new_order.user = self.request.user
        new_order.source_port = self.request.POST["source_port"]
        new_order.dest_port = self.request.POST["dest_port"]
        new_order.transportation_by = self.request.POST["transportation_by"]
        if self.request.POST["transportation_by"] == "fcl":
            new_order.container_type = self.request.POST["container_type"]
            new_order.container_quantity = len(self.request.POST["selected_container"].split(","))
        else:
            new_order.pkg_weight = self.request.POST["pkg_weight"]
            new_order.pkg_volume = self.request.POST["pkg_volume"]
            new_order.pkg_quantity = int(self.request.POST["pkg_quantity"])
        new_order.shipping_date = self.request.POST["shipping_date"]
        new_order.consignee_name = self.request.POST["consignee_name"]
        new_order.booked_container = self.request.POST["selected_container"]
        new_order.total_amt = self.request.POST["total_amt"]
        new_order.save()
        return redirect("home")


class MyShipment(LoginRequiredMixin, TemplateView):
    template_name = 'my_shipment.html'
    login_url = reverse_lazy("login")
    extra_context = {}

    def get(self, *args, **kwargs):
        self.extra_context["orders"] = Order.objects.filter(
            user=self.request.user).order_by("-id")
        if self.extra_context["orders"]:
            return super().get(self, *args, **kwargs)
        else:
            return redirect("book_shipping_containers")


@csrf_exempt
def getBookedContainerList(request):
    response = {"status": 405, "data": "Method Not Allowed"}
    if request.method == "POST":
        source_port = request.POST["source_port"]
        dest_port = request.POST["dest_port"]
        shipping_date = request.POST["shipping_date"]
        if source_port and dest_port and shipping_date:
            shipping_date = datetime.strptime(shipping_date, "%Y-%m-%d").date()
            order_obj = Order.objects.filter(
                source_port=source_port, dest_port=dest_port, shipping_date=shipping_date)
            booked_container_list = ""
            for order in order_obj:
                booked_container_list += order.booked_container
            response["status"] = 200
            response["data"] = booked_container_list
    return JsonResponse(response)


@csrf_exempt
def getServiceChargeView(request):
    response = {"status": 405, "data": "Method Not Allowed"}
    if request.method == "POST":
        source_port = request.POST["source_port"]
        dest_port = request.POST["dest_port"]
        service_charge = getServiceCharge(source_port, dest_port)
        response["status"] = 200
        response["charge"] = service_charge
    return JsonResponse(response)


@csrf_exempt
def getContainerChargeView(request):
    response = {"status": 405, "data": "Method Not Allowed"}
    if request.method == "POST":
        transportation_by = request.POST["transportation_by"]
        container_type = request.POST["container_type"]
        weight = request.POST["weight"]
        volume = request.POST["volume"]
        quantity = int(request.POST["quantity"])
        service_charge = float(request.POST["service_charge"])
        container_charge, subtotal = getContainerCharge(
            transportation_by, container_type, weight, volume, quantity)
        response["status"] = 200
        response["charge"] = container_charge
        response["subtotal"] = subtotal
        response["total"] = subtotal + service_charge
    return JsonResponse(response)
