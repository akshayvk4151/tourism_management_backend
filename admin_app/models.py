from django.db import models

# Create your models here.


class Blog(models.Model):
    Blog_topic = models.CharField(max_length=200)
    post_date = models.DateField()
    blog_description = models.CharField(max_length=800)
    blog_image = models.ImageField(upload_to='blog/')

    class Meta:
        db_table = 'blog_tb'

class Destination(models.Model):
    place = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    bus_price = models.IntegerField()
    train_price = models.IntegerField()     
    flight_price = models.IntegerField()
    image1 = models.ImageField(upload_to= 'destination/')
    image2 = models.ImageField(upload_to= 'destination/')
    image3 = models.ImageField(upload_to= 'destination/')
    image4 = models.ImageField(upload_to= 'destination/')
    food_price = models.IntegerField()
    number_of_person = models.IntegerField()
    days = models.CharField(max_length=30)
    nights = models.CharField(max_length=30)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'destination_tb'

