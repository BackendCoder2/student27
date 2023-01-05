from django.db import models
from django.conf import settings
from base.models import TimeStamp,UserFK
from users.models import Profile
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

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
  
    AVAILABLE = 'AV'
    PROGRESS = 'PR'
    REVIEW = 'RW'
    REVISION = 'RV'
    CLOSED = 'CL'

    
    STAGE = [
        (AVAILABLE, 'available'),        
        (PROGRESS, 'in-progress'),      
        (REVIEW, 'in-review'),
        (REVISION, 'in-revision'),
        (CLOSED, 'closed'),
    ]
    
    
    #ticket = models.IntegerField(blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    
    title = models.CharField(help_text="Write Short job tittle here",max_length=255, blank=True, null=True)
    description = models.TextField(help_text="Write Details job delivarables  here",blank=True, null=True)
   # dfile = models.FileField(blank=True, null=True)
    
    price = models.FloatField(help_text="Enter amount to pay per page-KES",blank=True, null=True)
    quantity = models.IntegerField(help_text="Enter number of pages required",blank=True, null=True)
    
    finished_at = models.DateTimeField(help_text="Enter submission Deadline.Tip- Enter time less than the actual! ",blank=True, null=True)    
    
    display = models.BooleanField(help_text="Check this button to make your job available in the market/dashboard",default=False, blank=True)    
    #closed = models.BooleanField(default=False, blank=True)
    
    state = models.BooleanField(default=None, blank=True, null=True)
    
    
    status = models.CharField(
        max_length=100,
        choices=STAGE,
        default=AVAILABLE,
    )    
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return "JOB-ID: "+str(self.pk)+" :"+self.title

    class Meta:
        db_table = "e_jobs"
        
          
             
    @property
    def bids(self):
        return self.jobs(self).count()    
        
    @property
    def tprice(self):
        return self.quantity*self.price    
        
    @classmethod    
    def jobs(cls,job):
        return cls.objects.filter(bid__job=job)  
                        
                
class Bid(UserFK,TimeStamp):#(models.Model):      
    job= models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    #name = models.CharField(max_length=100, default="pending", blank=True, null=True)
    
    approve = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True,null=True) #job_owner   
    accept = models.BooleanField(help_text="FOR TASKER",default=False, blank=True,null=True)#by_bidder
    
    def __str__(self):
        return str(self.job)
        
    @property    #    
    def profile(self):
        return Profile.objects.get(user=self.user)
                
    @property        
    def user_ratings(self):
        return str(self.profile.rating)
        
    @property        
    def user_job_in_progress(self):
        return str(self.profile.job_in_progress)
        
    @property                        
    def user_jobs_in_revision(self):
        return str(self.profile.job_disputed) 
        
    @property         
    def user_job_completed(self):
        return str(self.profile.rating) 
              
    @property        
    def user_job_disputed(self):
        return str(self.profile.job_disputed)
    @property        
    def approved(self):
        return self.approve  
        
    class Meta:
        db_table = "e_bids"
        #unique_together = ['user', 'job']
        ordering = ("created_at",) 
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.bidder=self.user  
            
        print("STATUSSSS:",self.job.status)  
        print("APPRD:",self.approved)
        print("APPR:",self.approve)
        print("ACCEPT:",self.accept)
     
        if self.accept and not self.approve:
            self.accept=False
 
                       
            
        #self.user=User.objects.get(id=self.bidder_id)    

        if self.approve and self.accept:# and self.job.assigned_to is None:
            Job.objects.filter(id=self.job.id).update(assigned_to=self.user,state=True)
            
        super().save(*args, **kwargs)
        
        
class Submission(UserFK,TimeStamp):
    REVIEW = 'RVW'
    REVISE = 'RVS'
    
    REJECTED= 'RJ'
    SUCCESS = 'SC'
    
    STATUS = [
        (REVIEW, 'review'),   
        (REVISE, 'Revise'),
        (REJECTED, 'Rejected'),
        (SUCCESS, 'Success'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    proof = models.TextField()
    # dfile = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=250, default="pending", blank=True, null=True) # approved, revise, pending,rejected

    feedback = models.CharField(
        max_length=100,
        choices=STATUS,
        default=REVIEW,
    )
        
    def __str__(self):
        return f"Submission:{self.id} for "+str(self.job)
        
    def get_absolute_url(self):
        return reverse('submission-list', kwargs={'pk': self.pk})        

    class Meta:
        db_table = "e_submissions"

    
