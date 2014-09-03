import datetime

from django.db import models
from django.conf import settings

class UserRegistration(models.Model):

    user_name = models.CharField(max_length=80, db_column="user_name", null=False)
    creation_time = models.DateTimeField(db_column="term", null=False)
    
    def __unicode__(self):
        return self.user_name + '(' + self.id + ')'
    
    class Meta:
        ordering = ["creation_time"]
        app_label = 'user_statistics'
        db_table = 'user_statistics_registration'
        managed = False if not settings.TEST_MODE else True
    
    @staticmethod
    def history():
        # Null dates will not be counted.
        history = UserRegistration.objects.exclude(creation_time__isnull=True)
        # Invalid dates (e.g. 0000-00-00 00:00:00) will not be counted.
        history = [history_item for history_item in history if history_item.creation_time]
        history_items = []
        for record in history:
            item = {}
            item['user_name'] = record.user_name
            item['creation_time'] = record.creation_time.strftime('%Y-%m-%d %H:%M:%S')
            history_items.append(item)
        return history_items
    
    @staticmethod
    def frequency():
        # Null dates will not be counted.
        history = UserRegistration.objects.exclude(creation_time__isnull=True)
        # Invalid dates (e.g. 0000-00-00 00:00:00) will not be counted.
        history = [history_item for history_item in history if history_item.creation_time]
        
        # Build a sequence of dates covering the date range in question.
        # history is ordered by creation time so first and last date should give range.
        first = history[0]
        last = history[len(history) - 1]
        first_date = first.creation_time.date()
        last_date = last.creation_time.date()
        known_dates = dict()
        date = first_date
        while date <= last_date:
            known_dates[date] = 0
            date += datetime.timedelta(days = 1) 
          
        # Bin the registration date-times by day.   
        for record in history:
            creation_time = record.creation_time
            date = creation_time.date()
            if not date in known_dates:
                # Should not get here.
                known_dates[date] = 0
            known_dates[date] += 1
            
        # Restructure the data so it can be sent in JSON formated string.
        frequency_items = []
        for date in known_dates:
            item = {'date': date, 'count': known_dates[date]}
            frequency_items.append(item)
        # Data were stored in dictionary so not necessarily sorted by date, so resort by date.
        frequency_items = sorted(frequency_items, key=lambda item: item['date']) 
        # Convert all dates to string dates.
        for item in frequency_items:
            item['date'] = item['date'].strftime('%Y-%m-%d')
        return frequency_items
             
  
    @staticmethod
    def user_dict():
        # Null dates will not be counted.
        pairs = UserRegistration.objects.exclude(creation_time__isnull=True)
        # Invalid dates (e.g. 0000-00-00 00:00:00) will not be counted.
        pairs = [pair for pair in pairs if pair.creation_time]
        code_map = {}
        for pair in pairs:
            key = pair.user_name
            value = pair.creation_time.strftime('%Y-%m-%d %H:%M:%S')
            code_map[key] = value
        return code_map
  
