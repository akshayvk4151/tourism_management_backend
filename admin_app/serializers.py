from rest_framework import serializers

from admin_app.models import Blog, Destination


class blogserializer(serializers.ModelSerializer):


    class Meta:
        model = Blog
        fields = '__all__'


class Destination_serializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

        