from django import forms
from .models import City, Cleaners, Bookings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Enter your last name.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class BookingsForm(forms.Form):
    booking_date = forms.DateField()
    booking_time = forms.TimeField()
    customer_mobile_number = forms.CharField(max_length=10)

    class Meta:
        model = Bookings
        fields = ('bookings_date', 'bookings_time', 'customer_mobile_number')

    def clean_customer_mobile_number(self):
        mobile_number = self.cleaned_data.get('customer_mobile_number', '')
        if mobile_number:
            if len(mobile_number) == 10 :
                if all([x.isdigit() for x in mobile_number.split("-")]):
                    return mobile_number
            else:
                raise forms.ValidationError("Mobile number is not valid.")
        else:
            raise forms.ValidationError("Please enter a mobile number.")


class CleanersForm(forms.Form):
    mobile_number = forms.CharField(max_length=10)

    class Meta:
        model = Bookings
        fields = ('mobile_number')

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number', '')
        if mobile_number:
            if len(mobile_number) == 10 :
                if all([x.isdigit() for x in mobile_number.split("-")]):
                    return mobile_number
            else:
                raise forms.ValidationError("Mobile number is not valid.")
        else:
            raise forms.ValidationError("Please enter a mobile number.")    


# class CustomersForm(forms.Form):
#   first_name = forms.CharField(max_length=20)
#   last_name = forms.CharField(max_length=20)
#   mobile_number = forms.CharField(max_length=10)

#   class Meta:
#       model = Customers
#       fields = ('first_name', 'last_name', 'mobile_number')