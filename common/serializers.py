from rest_framework import serializers

from common.models import Admin, Booking, ContactUs, Customer

class Cuserializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class Adminserializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

