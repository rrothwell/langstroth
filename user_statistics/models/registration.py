from django.db import models
from django.conf import settings

class UserRegistration(models.Model):

    user_name = models.CharField(max_length=200, db_column="user_name", null=False)
    creation_time = models.DateTimeField(db_column="creation_time", null=False)
    
    def __unicode__(self):
        return self.user_name + '(' + self.id + ')'
    
    class Meta:
        ordering = ["user_name"]
        app_label = 'user_statistics'
        db_table = 'user_statistics_UserRegistration'
        managed = False if not settings.TEST_MODE else True
    
    # Find the list of allocations that have been approved, 
    # group them by name,
    # but then return just the latest in each allocation group.
    # The data needs some cleanup as there are some allocations with very similar names.
    @staticmethod
    def history():
        return UserRegistration.objects.all()      
    
