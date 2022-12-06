from django.db import models
from django.conf import settings
from base.models import TimeStamp,UserFK
from django.urls import reverse

class Category(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100, default="Others", blank=True, null=True) 
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "e_categories"
        verbose_name_plural = "Categories"
        
class SubCategory(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100, default="Others", blank=True, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name
        
    def __str__(self):
        return self.name +" of " + str(self.category)+" Category"

    class Meta:
        db_table = "e_subcategories"
        verbose_name_plural = "Sub Categories"
                
class Type(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100, default="escrew", blank=True, null=True) 
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "e_types"   
             
class Status(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100, default="pending", blank=True, null=True) 
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "e_status"
        verbose_name_plural = "Status"
                    
class Job(UserFK,TimeStamp):    
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    ttype = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
   # dfile = models.FileField(blank=True, null=True)
    
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    approved = models.BooleanField(default=True, blank=True)    
    closed = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "e_jobs"
        
    @property    
    def status(self):
        if self.closed:
            return "CLOSED"
        elif  self.approved and not self.closed:
            return "OPEN"
        else:
            return "BOOKED"        
                

class Submission(UserFK,TimeStamp):

    PENDING = 'PG'
    REVISE = 'RV'
    REJECTED= 'RJ'
    SUCCESS = 'SC'
    
    STATUS = [
        (PENDING, 'Pending'),
        (REVISE, 'Revise'),
        (REJECTED, 'Rejected'),
        (SUCCESS, 'Success'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    proof = models.TextField()
    # dfile = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=100, default="pending", blank=True, null=True) # approved, revise, pending,rejected

    feedback = models.CharField(
        max_length=2,
        choices=STATUS,
        default=PENDING,
    )

        
    def __str__(self):
        return f"Submission:{self.id} for "+str(self.job)
        
    def get_absolute_url(self):
        return reverse('submission-list', kwargs={'pk': self.pk})        

    class Meta:
        db_table = "e_submissions"
