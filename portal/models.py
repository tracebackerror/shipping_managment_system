from django.db import models
from django.contrib.auth.models import User
import random

def randomOTP():
    return random.randrange(1111,9999)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    source_port = models.CharField(max_length=250,null=True)
    dest_port = models.CharField(max_length=250,null=True)
    transportation_by = models.CharField(max_length=3,default="fcl")
    container_type = models.CharField(max_length=100,null=True)
    container_quantity = models.PositiveBigIntegerField(default=0)
    pkg_weight = models.CharField(max_length=50,default="0")
    pkg_volume = models.CharField(max_length=50,default="0")
    pkg_quantity = models.PositiveBigIntegerField(default=0)
    shipping_date = models.DateField()
    delivery_date = models.DateField(null=True)
    delivery_otp = models.IntegerField(default=randomOTP)
    consignee_name = models.CharField(max_length=100)
    booked_container = models.CharField(max_length=500)
    total_amt = models.CharField(max_length=50,default=0)

    def __str__(self) -> str:
        return f"{self.id} - {self.user}"