from django.db import models

class Table(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    qty = models.IntegerField()
    busy = models.BooleanField(default=False)

class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    content = models.TextField()
    active = models.BooleanField(default=True)
    water = models.BooleanField(default=False)

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20)
    peopleQty = models.IntegerField()
    date = models.DateTimeField()
    tables = models.ManyToManyField(Table)
    confirmed = models.BooleanField(default=False)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20)
