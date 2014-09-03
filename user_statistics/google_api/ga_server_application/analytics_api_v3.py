#!/usr/bin/python
# -*- coding: utf-8 -*-

# Original licensed by Google under the Apache 2.0 License.

# For an over view see: https://developers.google.com/analytics/devguides/reporting/core/v3/
# For getting started see: https://developers.google.com/analytics/resources/tutorials/hello-analytics-api
# For a description of the API syntax see: https://developers.google.com/analytics/devguides/reporting/core/v3/reference
# For a description of the dimensions and metrics see: https://developers.google.com/analytics/devguides/reporting/core/dimsmets

from datetime import date

# import the Auth Helper class
import analytics_api_v3_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

ANALYTICS_START_DATE = '2013-08-08'
PRINT_LABEL_TEMPLATE = 'New users on: %s: %s'
PRINT_TOTAL_TEMPLATE = 'Total new users over period: %d'

def new_users():
    
    results = []
    
    # Step 1. Get an analytics service object.
    service = analytics_api_v3_auth.initialize_service()
    
    try:
        # Step 2. Get the user's first profile ID.
        profile_id = get_first_profile_id(service)
        
        if profile_id:
            # Step 3. Query the Core Reporting API.
            results = get_results(service, profile_id)
            
            # Step 4. Output the results.
            # print_results(results)
        
    except TypeError, error:
        # Handle errors in constructing a query.
        print ('There was an error in constructing your query : %s' % error)
        
    except HttpError, error:
        # Handle API errors.
        print ('Arg, there was an API error : %s : %s' % (error.resp.status, error._get_reason()))
        
    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
        'the application to re-authorize')
        
    return results.get('rows')
        
def get_first_profile_id(service):
    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()
    
    if accounts.get('items'):
        # Get the first Google Analytics account
        first_account_id = accounts.get('items')[0].get('id')
        
        # Get a list of all the Web Properties for the first account
        web_properties = service.management().webproperties().list(accountId=first_account_id).execute()
        
        if web_properties.get('items'):
            # Get the first Web Property ID
            first_web_property_id = web_properties.get('items')[0].get('id')
            
            # Get a list of all Views (Profiles) for the first Web Property of the first Account
            profiles = service.management().profiles().list(accountId=first_account_id, webPropertyId=first_web_property_id).execute()
            
            if profiles.get('items'):
                # return the first View (Profile) ID
                return profiles.get('items')[0].get('id')
    
    return None

# See: https://developers.google.com/analytics/devguides/reporting/core/dimsmets#view=detail&group=user
def get_results(service, profile_id):
    current_end_date = date.today().strftime('%Y-%m-%d')
    # Use the Analytics Service Object to query the Core Reporting API
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date= ANALYTICS_START_DATE,
        end_date=current_end_date,
        metrics='ga:newUsers',
        dimensions='ga:date',
        sort='ga:date').execute()
        
def print_results(results):
    # Print data nicely for the user.
    if results:
        print 'First View (Profile): %s' % results.get('profileInfo').get('profileName')
        result_list = results.get('rows')
        print "Result count %s: " % len(result_list)
        total_new_users = 0
        for result in result_list:
            print PRINT_LABEL_TEMPLATE % (result[0], result[1])
            total_new_users += int(result[1])
        print PRINT_TOTAL_TEMPLATE % total_new_users        
    else:
        print 'No results found'
