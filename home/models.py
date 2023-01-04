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
   
   
class Index(models.Model):
    m1 =  models.CharField(default="Within deadlines",max_length=100, blank=True, null=True)
    m2 =  models.CharField(default="At low cost",max_length=100, blank=True, null=True)
    m3 =  models.CharField(default="At any Time",max_length=100, blank=True, null=True)
    m4 =  models.CharField(default="With perfection",max_length=100, blank=True, null=True)
    m5 =  models.CharField(default="",max_length=100, blank=True, null=True)
    m6 =  models.CharField(default="",max_length=100, blank=True, null=True)
    m7 =  models.CharField(max_length=100, blank=True, null=True)
    
    message1 = models.TextField(default="We complete your tasks,from essays or eBooks to programming.",max_length=100, blank=True, null=True)
    message2 = models.TextField(default="With the AjiraPanel Platform, you can post any digital task ,assignement of any difficulty to be done for you.Our high profile wtitters are ready to assist you.Welcome!",max_length=300, blank=True, null=True)
    message3 = models.TextField(default="AjiraPanel has evolved to a platform where employers and writers co-exist. Posting orders to the public and digital payment are the trending features. It still remains to be a tool for you to manage your writers effeciently. Comes with an inbuilt plagiarism checker, ability to assign and reasign orders, track payments and balances, among other incredible features. All bundled up for you to ensure you run your operations smoothly.",max_length=300, blank=True, null=True)
    message4 = models.TextField(default="AjiraPanel is an Platform that sorts out your digital task management problems, by offering the ability to manage all your taskers with ease.",max_length=300, blank=True, null=True)
    call =  models.CharField(default="0792966490",max_length=100, blank=True, null=True)

    class Meta:
        db_table = "d_index"
        verbose_name_plural = "EDIT HOMEPAGE"
   
    def __str__(self):
       return "EDIT INDEX/HOMEPAGE CONTENT"
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
        
    
