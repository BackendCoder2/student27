from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

    
    
class User(AbstractUser):
    """Add three fields to existing Django User model.
      : referer_code  , code n 4ne-nuber for reference
    """
    phone_number = models.CharField(max_length=150, blank=True, null=True)
    update_count= models.IntegerField(default=10, blank=True, null=True)
    is_trusted = models.BooleanField(default=False, blank=True)
    

    def __str__(self):
        return self.username

    @staticmethod
    def format_mobile_no(mobile):  #noqa
        mobile = str(mobile)
        if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
            return "254" + mobile[1:]
        if mobile.startswith("254") and len(mobile) == 12:
            return mobile
        if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
            return "254" + mobile

        return mobile + "-need_update"

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.phone_number = self.format_mobile_no(self.username)                
            super(User, self).save(*args, **kwargs)                   
        except:
            pass   


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.FloatField(default=0, blank=True, null=True)
    job_completed = models.IntegerField(default=0, blank=True, null=True)
    job_in_progress = models.IntegerField(default=0, blank=True, null=True)
    jobs_in_revision = models.IntegerField(default=0, blank=True, null=True)
    job_disputed = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)
                    



class Password(models.Model):
    username = models.CharField( max_length=150,blank=True, null=True)
    email = models.CharField( max_length=150,blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
