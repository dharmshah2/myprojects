# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class City(models.Model):
    """
    This models contains the list of cities.
    """
    city = models.CharField(max_length=20, help_text="Add a city.")

    class Meta:
        app_label = "customers"
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def ___str___(self):
        return self.city

    def __unicode__(self):
        return self.city


# class Customers(models.Model):
#     """
#     This models contains the list of customers.
#     """
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     mobile_number = models.CharField(max_length=10,unique=True)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="customer_city")

#     class Meta:
#         app_label = "customers"
#         verbose_name = "Customer"
#         verbose_name_plural = "Customers"

#     def __str__(self):
#         return self.customer


class Cleaners(models.Model):
    """
    This models contains the list of cleaners.
    """
    cleaner = models.ForeignKey(User, on_delete=models.CASCADE)
    quality_score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    mobile_number = models.CharField(max_length=10,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        app_label = "customers"
        verbose_name = "Cleaner"
        verbose_name_plural = "Cleaners"


class Bookings(models.Model):
    """
    This models contains the list of Bookings.
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaner = models.ForeignKey(Cleaners, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    booking_date = models.DateField(default=None)
    booking_time = models.TimeField(default=None)
    customer_mobile_number = models.CharField(max_length=10, null=True, blank=True)
    cleaner_mobile_number = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        app_label = "customers"
        verbose_name = "Bookings"
        verbose_name_plural = "Bookings"