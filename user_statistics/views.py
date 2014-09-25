import logging
from json import dumps
from django.http import HttpResponse
from django.shortcuts import render
from user_statistics.models.registration import UserRegistration

LOG = logging.getLogger('custom.debug')

# Web pages

def index_page(request):
    return trend_visualisation_page(request)

def trend_visualisation_page(request):
    context = {
        "title": "User Registrations",
        "tagline": ""}
    return render(request, "user_statistics.html", context)

# Web services with JSON pay loads.

def registrations_history(request):
    registration_history = UserRegistration.history()
    json_string = dumps(registration_history)
    LOG.debug("Registration history REST response: " + json_string)
    return HttpResponse(json_string, "application/json")

def registrations_frequency(request):
    # registration_frequency = UserRegistration.frequency()
    registration_frequency = UserRegistration.monthly_frequency()
    # Convert all dates to string dates.
    registrations = [{'date': UserRegistration.last_date_of_month(item['date']).strftime('%Y-%m-%d'), 'count': item['count']} for item in registration_frequency]
    # registration_frequency = GoogleAnalytics.frequency()
    json_string = dumps(registrations)
    LOG.debug("Registration frequency REST response: " + json_string)
    return HttpResponse(json_string, "application/json")

