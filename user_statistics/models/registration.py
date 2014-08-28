from django.db import models
from django.conf import settings

class UserRegistration(models.Model):

    user_name = models.CharField(max_length=80, db_column="user_name", null=False)
    creation_time = models.DateTimeField(db_column="creation_time", null=False)
    
    def __unicode__(self):
        return self.user_name + '(' + self.id + ')'
    
    class Meta:
        ordering = ["user_name"]
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
    def user_dict():
        pairs = UserRegistration.objects.all()
        code_map = {}
        for pair in pairs:
            key = pair.user_name
            value = pair.creation_time.strftime('%Y-%m-%d %H:%M:%S')
            code_map[key] = value
        return code_map
  
