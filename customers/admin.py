# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import City, Cleaners, Bookings


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ("city",)
    search_fields = ["city"]


# class CustomersAdmin(admin.ModelAdmin):

#     @staticmethod
#     def get_city(obj):
#         return obj.city.city

#     list_display = ("first_name", "last_name", "mobile_number", "get_city")
#     search_fields = ["city", "first_name", "mobile_number"]
#     list_filter = ("city",)


class CleanersAdmin(admin.ModelAdmin):
    list_display = ("cleaner", "quality_score", "mobile_number", "city")
    search_fields = ["city", "cleaner", "mobile_number"]
    list_filter = ("city__city", "quality_score")


class BookingsAdmin(admin.ModelAdmin):
    list_display = ("customer", "cleaner", "city", "booking_date", "booking_time", "customer_mobile_number", "cleaner_mobile_number")
    search_fields = ["customer", "cleaner"]
    list_filter = ("city__city",)


admin.site.register(City, CityAdmin)
# admin.site.register(Customers, CustomersAdmin)
admin.site.register(Cleaners, CleanersAdmin)
admin.site.register(Bookings, BookingsAdmin)