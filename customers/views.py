# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from .forms import CustomersForm
from .models import City, Bookings, Cleaners
from .forms import SignUpForm, BookingsForm, CleanersForm
import datetime

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        ## if form is valid then saving user details and logged in that user into the system.
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('dashboard')
    else:
        if request.user.username:
            return redirect('dashboard')
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/login')
def dashboard(request):
    """
    It will create a user if the request is POST else will show a signup form.
    """
    if request.method == "POST":
        form = BookingsForm(request.POST)
        
        if form.is_valid():

            customer_city = City.objects.get(id=request.POST.get('city'))
            customer_date = is_date_time_valid(
                                            request.POST.get('booking_date', ''), 
                                            request.POST.get('booking_time', '') 
                                         )

            ## if not formated date or past date
            if not customer_date:
                msg="Select a valid date & time."
                return render(request, 'success.html', {'msg':msg})

            is_cleaners_available_in_city = cleaner_availability_in_city(customer_city)

            ## if no cleaner available in a city
            if not is_cleaners_available_in_city:
                msg = "No cleaners are available in " + customer_city.city +  " city"
                return render(request, 'success.html', {'msg':msg})

            available_cleaners = available_cleaners_in_city(request, customer_city)


            if available_cleaners:
                customer_time = datetime.datetime.strptime(request.POST.get('booking_time'), '%H:%M').time()
                customer_date = datetime.datetime.strptime(request.POST.get('booking_date'), '%Y-%m-%d').date()
                customer_mobile_number = request.POST.get('customer_mobile_number')
                cleaner_mobile_number = Cleaners.objects.get(cleaner_id=available_cleaners[0]).mobile_number
                cleaner = Cleaners.objects.get(cleaner_id=available_cleaners[0])
                import pdb; pdb.set_trace()
                booking_obj = Bookings.objects.create(cleaner=cleaner,
                                        customer=request.user,
                                        city=customer_city,
                                        booking_date=customer_date, 
                                        booking_time=customer_time,
                                        customer_mobile_number=customer_mobile_number,
                                        cleaner_mobile_number=cleaner_mobile_number,
                                    )
                booking_obj.save()
            else:
                msg="No cleaners are available at this time."
                return render(request, 'success.html', {'msg':msg})

            msg="You have been appointed a cleaner " + cleaner.username
            return render(request, 'success.html', {'msg':msg})
        else:
            error_msg = form.errors[form.errors.keys()[0]]
        
            form = BookingsForm()
            cities = City.objects.all()
        
            return render(request, 'dashboard.html', {'error':error_msg, 'form':form, 'cities':cities})
    else:
        # form = CustomersForm()
        form = BookingsForm()
        cities= City.objects.all()
    return render(request, 'dashboard.html', {'form':form, 'cities':cities})


@login_required(login_url="/login")
def cleaner_view(request):
    if request.method == "POST":
        form = CleanersForm(request.POST)
        
        if form.is_valid():

            cleaner, created = Cleaners.objects.get_or_create(
                    cleaner=request.user, city=City.objects.get(id=request.POST.get('city'))
                )

            # in update or create we have to register or update mobile number
            cleaner.mobile_number = request.POST.get('mobile_number')
            cleaner.save()

            msg="You are successfully registed with us."
            return render(request, 'success.html', {'msg':msg})
        else:
            error_msg = form.errors[form.errors.keys()[0]]
        
            form = CleanersForm()
            cities = City.objects.all()
        
            return render(request, 'cleaner_detail.html', {'error':error_msg, 'form':form, 'cities':cities})
    else:
        form = CleanersForm()
        cities = City.objects.all()
        
        return render(request, 'cleaner_detail.html', {'form':form, 'cities':cities})


def cleaner_availability_in_city(customer_city):
    """
    We are checking here if cleaners are available in the city.
    """
    total_cleaners = Cleaners.objects.filter(city=customer_city).values_list("cleaner", flat=True)

    if not total_cleaners:
        return False
    else:
        return True


def available_cleaners_in_city(request, customer_city):
    """
    Here we are taking a customer city as arguments and returning total cleaners in customer city. 
    """
    available_cleaners = []

    total_cleaners = Cleaners.objects.filter(city=customer_city).values_list("cleaner", flat=True)

    customer_time = datetime.datetime.strptime(request.POST.get('booking_time'), '%H:%M').time()
    customer_date = datetime.datetime.strptime(request.POST.get('booking_date'), '%Y-%m-%d').date()

    for cleaner in total_cleaners:
        booked_cleaner = Bookings.objects.filter(cleaner=cleaner,
                             city=customer_city,
                             booking_date=customer_date, 
                             booking_time=customer_time
                            )
        if not booked_cleaner:
            available_cleaners.append(cleaner)

    return available_cleaners


def is_date_time_valid(str_date, str_time):
    """
    We will check here if date is exist or not
    """
    try:
        customer_date = datetime.datetime.strptime(str_date + " " + str_time, "%Y-%m-%d %H:%M")
        now = datetime.datetime.now()
        if customer_date >= now:
            return True
    except:
        return False