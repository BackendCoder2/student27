from django.db import models
from django.conf import settings
from base.models import TimeStamp,UserFK
from users.models import Profile
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

CC=["PR",'RW','RV']
CR=['RW','RV']

class Category(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100, default="Others", blank=True, null=True) 
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "e_categories"
        verbose_name_plural = "Categories"
        
class SubCategory(TimeStamp):#(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name
        
    def __str__(self):
        return self.name +" of " + sStr(self.category)+" Category"

    class Meta:
        db_table = "e_subcategories"
        verbose_name_plural = "Sub Categories"

class DFile(TimeStamp):#(models.Model):
    dfile = models.FileField(upload_to='media/documents/%Y/%m/%d/',blank=True, null=True)
    description = models.CharField(help_text="Write Short File description here",max_length=255, blank=True, null=True)
    def __str__(self):
        return "FILE"+str(self.id)+':' +self.description         
        
class RevInfo(TimeStamp):#(models.Model):
    dfile= models.ForeignKey(DFile, on_delete=models.CASCADE, blank=True, null=True)#
    description = models.TextField(help_text="FOR EMPLOYER.Write Details revision details  here",blank=True, null=True)
    def __str__(self):
        return "Rev:"+str(self.id)+':' +self.description      
        
                           
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
    
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    
    title = models.CharField(help_text="Write Short job tittle here",max_length=255, blank=True, null=True)
    description = models.TextField(help_text="Write Details job delivarables  here",blank=True, null=True)
    dfile = models.ForeignKey(DFile,help_text="Upload files from your device", on_delete=models.CASCADE, blank=True, null=True)#
    #dfile = models.FileField(blank=True, null=True)
    
    price = models.FloatField(help_text="Enter amount to pay per page-KES",blank=True, null=True)
    quantity = models.IntegerField(help_text="Enter number of pages required",blank=True, null=True)
    
    finished_at = models.DateTimeField(help_text="Enter submission Deadline.Tip- Enter time less than the actual! ",blank=True, null=True)    
    
    display = models.BooleanField(help_text="Check this button to make your job available in the market/dashboard",default=False, blank=True)    
    #closed = models.BooleanField(default=False, blank=True)
    
    ###REVISION-STATUS
    #revise = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True)
    revise_info = models.ForeignKey(RevInfo,help_text="ADD file to put this job in revision", on_delete=models.CASCADE, blank=True, null=True)##DN   
    ###  

    ###CLOSED-STATUS
    accepted = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True)
    rejected = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True)
    rejection_description = models.TextField(help_text="FOR EMPLOYER.Write Details why you reject the work done by  tasker  here",blank=True, null=True)
    rejected_work_accepted = models.BooleanField(help_text="FOR TASKER,SUPPORT OR ADMIN.Admin to decide if the tasker refused to ACCEPT",default=False, blank=True)    
    ###    
    
    
    status = models.CharField(
        max_length=100,
        choices=STAGE,
        default=AVAILABLE,
    )    
    
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employers",
        blank=True,
        null=True,
    )    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="writters",
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return "JOB-ID: "+str(self.pk)+" :"+self.title

    @property
    def time_remaining(self):
        now=self.finished_at-timezone.now()
   
        return now	   
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
                

    def complete_order(self):
        #TODO
        pass
        #return "PAY-PAY"   

    def explain_n_raise_complain(self):
        #TODO
        pass
        #return "NO-PAY"  
                                
    def save(self, *args, **kwargs):
        if not self.pk:
            self.employer=self.user       
                    
        if self.accepted and self.status in CC:
            self.complete_order()
            self.status="CL"

        if self.revise_info and self.status =="RW":   
            print("IKOOO_RRRE")     
            Job.objects.filter(id=self.id).update(status="RV") 

        if self.rejected and not self.accepted and self.status in CC:
             
            if not self.rejection_description:
                return
            if self.rejected_work_accepted:
                self.status="CL"
                #self.explain_n_raise_complain()
            
        super().save(*args, **kwargs)   
        
        
        
class Bid(UserFK,TimeStamp):#(models.Model):      
    job= models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    
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
        
    class Meta:
        db_table = "e_bids"
        #unique_together = ['user', 'job']
        ordering = ("created_at",) 
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.bidder=self.user  
                        
        print("STATUSSSS:",self.job.status)    
        print("APPR:",self.approve)
        print("ACCEPT:",self.accept)
     
        if self.accept and not self.approve:
            self.accept=False                        
            
        #self.user=User.objects.get(id=self.bidder_id)    

        if self.approve and self.accept:# and self.job.assigned_to is None:
            Job.objects.filter(id=self.job.id).update(assigned_to=self.user,display=False,status="PR")
            
        super().save(*args, **kwargs)
        
        
class Submission(UserFK,TimeStamp):

    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    proof = models.TextField()
    dfile = models.ForeignKey(DFile, on_delete=models.CASCADE, blank=True, null=True)#
    final = models.BooleanField(help_text="DRAFT/FINAL",default=False, blank=True)#by_bidder

        
    def __str__(self):
        return f"Submission:{self.id} for "+str(self.job)
        
    class Meta:
        db_table = "e_submissions"
        
    def save(self, *args, **kwargs):   
    
        if self.final:#draft
        
            Job.objects.filter(id=self.job.id).update(status="RW")   
            
        super().save(*args, **kwargs)
    
