from django.db import models
from datetime import datetime

def filter_html_elements(content):
    #TODO
    return content


class ContactUs(models.Model):
    cmail =  models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "d_contact_us"
        verbose_name_plural = "Contact Us Messages"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.message=filter_html_elements(self.message)#avoid XSS attack 
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)    

class UserStat(models.Model):
    homepage_hits_login =  models.IntegerField(default=0, blank=True, null=True)
    homepage_hits_anonymous = models.IntegerField(default=0, blank=True, null=True)
    spinx_hits = models.IntegerField(default=0, blank=True, null=True)
    spinx_hits_anonymous = models.IntegerField(default=0, blank=True, null=True)
    #s_date=models.DateTimeField(default=datetime.now(), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        db_table = "d_user_stat"
        get_latest_by ="id"
        
    def __str__(self):
        return "User Stats-"+str(self.id)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
        
    
