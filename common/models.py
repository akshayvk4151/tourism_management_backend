from django.db import models

from admin_app.models import Destination

# Create your models here.

class Customer(models.Model):
    customer_name = models.CharField(max_length=20)
    customer_phone = models.BigIntegerField()
    customer_address = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=30)
    customer_password = models.CharField(max_length=40, default='')
    profile_pic = models.ImageField(upload_to='customer/',default='static/images/dummy-user.png')
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'customer_tb'

class Admin(models.Model):
    admin_name = models.CharField(max_length=20)
    admin_email = models.CharField(max_length=30)
    admin_password = models.CharField(max_length=40, default='')

    class Meta:
        db_table = 'admin_tb'


class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = 'contact_tb'



class Booking(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    travel_mode = models.CharField(max_length=100, choices=[('bus', 'Bus'), ('train', 'Train'), ('flight', 'Flight')])
    travel_food = models.BooleanField(default=False)
    travel_date = models.DateField()
    travel_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,default="")

    class Meta:
        db_table = 'booking_tb'
        