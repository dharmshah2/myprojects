# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import City, Customers, Cleaners, Bookings


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ("city",)
    search_fields = ["city"]


class CustomersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "mobile_number", "city")
    search_fields = ["city", "first_name", "mobile_number"]
    list_filter = ("city",)


class CleanersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "quality_score", "mobile_number", "city")
    search_fields = ["city", "first_name", "mobile_number"]
    list_filter = ("city", "quality_score")


class BookingsAdmin(admin.ModelAdmin):
    list_display = ("customer", "cleaner", "city", "date", "start_time", "end_time")
    search_fields = ["customer", "cleaner"]
    list_filter = ("city",)


admin.site.register(City, CityAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Cleaners, CleanersAdmin)
admin.site.register(Bookings, BookingsAdmin)