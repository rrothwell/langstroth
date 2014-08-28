from django.db import models
from django.conf import settings

class UserRegistration(models.Model):

    user_name = models.CharField(max_length=80, db_column="user_name", null=False)
    creation_time = models.DateTimeField(db_column="creation_time", null=False)
    
    def __unicode__(self):
        return self.user_name + '(' + self.id + ')'
    
    class Meta:
        ordering = ["creation_time"]
        app_label = 'user_statistics'
        db_table = 'user_statistics_registration'
        managed = False if not settings.TEST_MODE else True
    
    @staticmethod
    def history():
        history = UserRegistration.objects.all()
        history_items = []
        for record in history:
            item = {}
            item['user_name'] = record.user_name
            item['creation_time'] = record.creation_time.strftime('%Y-%m-%d %H:%M:%S')
            history_items.append(item)
        return history_items
    
    @staticmethod
    def frequency():
        history = UserRegistration.objects.all()
        known_dates = dict()
        for record in history:
            date = record.creation_time.date()
            if not date in known_dates:
                known_dates[date] = 0
            known_dates[date] += 1
        frequency_items = []
        for date in known_dates:
            item = {'date': date, 'count': known_dates[date]}
            frequency_items.append(item)
        # Dictionary values so longer sorted by date so sort by date.
        frequency_items = sorted(frequency_items, key=lambda item: item['date']) 
        # Convert all dates to string dates.
        for item in frequency_items:
            item['date'] = item['date'].strftime('%Y-%m-%d')
        return frequency_items
             
  
    @staticmethod
    def user_dict():
        pairs = UserRegistration.objects.all()
        code_map = {}
        for pair in pairs:
            key = pair.user_name
            value = pair.creation_time.strftime('%Y-%m-%d %H:%M:%S')
            code_map[key] = value
        return code_map
  
