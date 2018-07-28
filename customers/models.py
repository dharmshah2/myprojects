# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


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

    def _str_(self):
        return self.city


class Customers(models.Model):
    """
    This models contains the list of customers.
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=10,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        app_label = "customers"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def _str_(self):
        return self.first_name


class Cleaners(models.Model):
    """
    This models contains the list of cleaners.
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    quality_score = models.DecimalField(max_digits=2, decimal_places=1)
    mobile_number = models.CharField(max_length=10,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        app_label = "customers"
        verbose_name = "Cleaner"
        verbose_name_plural = "Cleaners"

    def _str_(self):
        return self.first_name


class Bookings(models.Model):
    """
    This models contains the list of Bookings.
    """
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    cleaner = models.ForeignKey(Cleaners, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)

    class Meta:
        app_label = "customers"
        verbose_name = "Bookings"
        verbose_name_plural = "Bookings"

    def _str_(self):
        return self.customer

    @property
    def customer_mobile_number(self):
        return self.customer.mobile_number

    @property
    def cleaner_mobile_number(self):
        return self.cleaner.mobile_number