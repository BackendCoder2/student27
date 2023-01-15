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
        return self.name +" of " + str(self.category)+" Category"

    class Meta:
        db_table = "e_subcategories"
        verbose_name_plural = "Sub Categories"


        
                           
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
    order_id = models.IntegerField(blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    
    title = models.CharField(help_text="Write Short job tittle here",max_length=255, blank=True, null=True)
    description = models.TextField(help_text="Write Details job delivarables  here",blank=True, null=True)
    
    #dfile = models.FileField(blank=True, null=True)
    
    price = models.FloatField(help_text="Enter amount to pay per page-KES",blank=True, null=True)
    quantity = models.IntegerField(help_text="Enter number of pages required",blank=True, null=True)
    
    finished_at = models.DateTimeField(help_text="Enter submission Deadline.Tip- Enter time less than the actual! ",blank=True, null=True)    
    
    display = models.BooleanField(help_text="Check this button to make your job available in the market/dashboard",default=False, blank=True)    
    #closed = models.BooleanField(default=False, blank=True)
    
    ###REVISION-STATUS
    revise = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True)
     
    ###  

    ###CLOSED-STATUS
    accepted = models.BooleanField(help_text="FOR EMPLOYER",default=False, blank=True)
    rejected = models.BooleanField(help_text="FOR EMPLOYER.You need to provide rejection_description",default=False, blank=True)
    rejection_description = models.TextField(help_text="FOR EMPLOYER.Write Details why you reject the work done by  tasker  here",blank=True, null=True)
    rejected_work_accepted = models.BooleanField(help_text="FOR TASKER,SUPPORT OR ADMIN.Admin to decide if the tasker refused to ACCEPT",default=False, blank=True)    
    ###   
    paid = models.BooleanField(default=False, blank=True,null=True)
    
    
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
        return "JOB:Order-ID: "+str(self.order_id)+" :"
        
    class Meta:
    
        get_latest_by = ['id',]

    @property
    def time_remaining(self):        
        try:
            return  self.finished_at-timezone.now()                    
        except:
            return 0	   
           
    class Meta:
        db_table = "e_jobs"                  
             
    @property
    def bids(self):
        return self.jobs(self).count()    
        
    @property
    def tprice(self):
        return self.quantity*self.price 
    @property
    def tprice(self):        
        try:
            return  self.quantity*self.price                 
        except:
            return 0	   
                   
        
    @property
    def accepted_job(self):
        if self.accepted :               
            return "Accepted"
        return "Rejected" 
        
    @property
    def payment(self):
        if self.paid :               
            return "Paid"
        if self.paid is None:             
            return "Pending"  
        if self.paid is False:             
            return "Not-Paid"  
        
    @classmethod    
    def jobs(cls,job):

        try:
            return cls.objects.filter(bid__job=job)  
        except:
            return 0    
        
    @classmethod    
    def max_id(cls):
        try:
            return cls.objects.latest("id").id  
        except:
            return 0
    @property
    def biggest_id(self):
        return self.max_id()
        
    def complete_order(self):   
    
        try:
            employer_account=Account.objects.get(user=self.employer)
            writter_account=Account.objects.get(user=self.assigned_to)
            amount=self.tprice
            employer_account.transfer_tokens(self, writter_account, amount)
            self.paid=True
        except:
            pass
        
        
        #return "PAY-PAY"   

    def explain_n_raise_complain(self):
        #TODO
        pass
        #return "NO-PAY"  
                                
    def save(self, *args, **kwargs):
        if not self.pk:
            self.employer=self.user
          
            self.order_id=10000+self.biggest_id+1
                    
        if self.accepted and self.status in CC and not self.paid:
            
            self.complete_order()
            self.status="CL"
            

        if self.revise and self.status =="RW":   
            print("IKOOO_RRRE")     
            #Job.objects.filter(id=self.id).update(status="RV") 
            self.status="RV"
            
            self.save()

        if self.rejected and not self.accepted and self.status in CC:
             
            if not self.rejection_description:
                return
            if self.rejected_work_accepted:
                self.status="CL"
                self.paid=False
                #self.explain_n_raise_complain()
            
        super().save(*args, **kwargs)   
        
    #class Meta:
    #      constraints = [
    #         #models.CheckConstraint(check=models.Q(rejected!=None), rejection_description!=None,violation_error_message="NEED_REPLA"),
    #      ]  
        
        


       
        
         
class Bid(UserFK,TimeStamp):#(models.Model):      
    job= models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    
    approve = models.BooleanField(help_text="Check to Accept & Save/Submit(FOR EMPLOYER)",default=False, blank=True) #job_owner   
    accept = models.BooleanField(help_text="Check to Accept & Save/Submit(FOR TASKER)",default=False, blank=True)#by_bidder
    
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
        return str(self.profile.job_completed) 
              
    @property        
    def user_job_disputed(self):
        return str(self.profile.job_disputed)
        
    @property        
    def user_job_active(self):
        return self.user_job_in_progress+self.user_jobs_in_revision
    @property
    def accepted(self):
        if self.accept :               
            return "Accepted"
        return "Not Yet Accepted"         
        
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
            Job.objects.filter(id=self.job.id).update(assigned_to=self.bidder,display=False,status="PR")
            
        super().save(*args, **kwargs)
        
        
class Submission(UserFK,TimeStamp):
    sender= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    proof = models.TextField()    
    document = models.FileField(upload_to='media/documents/%Y/%m/%d/',blank=True, null=True)
    final = models.BooleanField(help_text="Check for Final Submission",default=False, blank=True)#by_bidder
    

        
    def __str__(self):
        return f"Submission:{self.id} for "+str(self.job)
        
    class Meta:
        db_table = "e_submissions"
        
    def save(self, *args, **kwargs): 
        if not self.pk:
            self.sender=self.user     
        if self.final:#draft
        
            Job.objects.filter(id=self.job.id).update(status="RW")   
            
        super().save(*args, **kwargs)
        
        
        
class RevInfo(TimeStamp):#(models.Model): 
    title = models.CharField(help_text="Write Short title here",max_length=255, blank=True, null=True)
    job = models.ForeignKey(Job,on_delete=models.CASCADE, blank=True, null=True) 
    document = models.FileField(upload_to='media/documents/%Y/%m/%d/',blank=True, null=True)
    description = models.TextField(help_text="FOR EMPLOYER.Write Details revision details  here",blank=True, null=True)
    def __str__(self):
        return "Rev:"+str(self.id)+':' +self.description    
                
        
class DFile(TimeStamp):#(models.Model):
    title = models.CharField(help_text="Write Short  title here",max_length=255, blank=True, null=True)
    job = models.ForeignKey(Job,help_text="Upload files from your device", on_delete=models.CASCADE, blank=True, null=True)#
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, blank=True, null=True)#
    rfile= models.ForeignKey(RevInfo, on_delete=models.CASCADE, blank=True, null=True)#
    
    dfile = models.FileField(upload_to='media/documents/%Y/%m/%d/',blank=True, null=True)
    description = models.CharField(help_text="Write Short File description here",max_length=255, blank=True, null=True)
    def __str__(self):
        return "FILE"+str(self.job.title)+':' +str(self.job.order_id)
        

