import logging

import requests
from django.conf import settings
import nagios

LOG = logging.getLogger('custom.debug')

def get_availability(start_date, end_date):
    url = settings.NAGIOS_AVAILABILITY_URL
    LOG.debug("Availability URL: " + url)
    resp = requests.get(url, auth=settings.NAGIOS_AUTH)
    LOG.debug("Availability response: " + resp.text)
    return nagios.parse_availability(resp.text)

def get_status():
    url = settings.NAGIOS_STATUS_URL
    resp = requests.get(url, auth=settings.NAGIOS_AUTH)
    return nagios.parse_status(resp.text)

# Monkey patch the production code so it will work
# in the non-production (test and uat) environments.
nagios.get_availability = get_availability
nagios.get_status = get_status
