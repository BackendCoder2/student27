from django.contrib import admin
from .models import Category,SubCategory,Job,Submission,Type,Bid,RevInfo,DFile
#from users.models import User
from .forms import JobForm,BidForm

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Type)
admin.site.register(DFile)
#admin.site.register(RevInfo)
#admin.site.register(Submission)


class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = (
        "id",
       # "user",
        "employer",
        "assigned_to",
        "sub_category",
        "title",
        "description",
        "dfile",
        "finished_at",
        "time_remaining",
        "status",
        "display",
        "bids",        
        #POST_WORK
        "accepted",
        "rejected",
        "rejection_description",
        "rejected_work_accepted"
    )

    list_display_links = ("id","sub_category","title",)
    list_filter = ("sub_category__category__name","status","display")
    search_fields = ('id',"sub_category__category__name","sub_category__name",)
    list_editable = (
        "status",
        "display",
        "finished_at",
        "employer",
        #"rejected",
        #"rejection_description",
        #"rejected_work_accepted"
        
    )
    
    read_only = ("status","assigned_to") 
    
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:     
            qs = self.model.objects.filter(employer=request.user)#_default_manager.get_queryset()  
              
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs    
        
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.user=request.user#ADD
        obj.save()
                
admin.site.register(Job, JobAdmin)




class BidAdmin(admin.ModelAdmin):
    form = BidForm
    list_display = (
        "id",
        #"user",        
        "bidder",
        "approve",
        "accept",
        "created_at",
        "job",
        "description",
        "user_ratings",
        "user_job_completed",
        "user_job_in_progress",
        "user_jobs_in_revision",
        "user_job_disputed"

    )

    list_display_links = ("id","job")
    list_filter = ("id","job__title","job__employer","user__username","user__profile__rating","user__profile__jobs_in_revision","user__profile__job_in_progress")
    search_fields = ("job__title","user__username")
    list_editable = (
        "approve",
        "accept",   
    )
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:
            qs = self.model.objects.filter(job__employer=request.user) | self.model.objects.filter(bidder=request.user)
            
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs  
        
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.user=request.user#ADD
        obj.save()        
            
admin.site.register(Bid, BidAdmin)




class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "proof",
        "dfile"
    )

    list_display_links = ("id","job")
    list_filter = ("user","job__title",)
    search_fields = ("user","job__title")
    list_editable = (
        "proof",
    )
    
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:                  
            qs = self.model.objects.filter(job__employer=request.user)  
              
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs 
              
admin.site.register(Submission, SubmissionAdmin)

class RevInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "dfile",
    )

    list_display_links = ("id",)
    list_filter = ("id",)
    search_fields = ("user","job__title")
    list_editable = (
        "description",
    )
    
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:                  
            qs = self.model.objects.filter(job__employer=request.user)  
              
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs 
              
admin.site.register(RevInfo, RevInfoAdmin)

