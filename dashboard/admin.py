from django.contrib import admin
from .models import Category,SubCategory,Job,Submission,Status,Type,Bid
#from users.models import User
from .forms import JobForm,BidForm

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Type)
admin.site.register(Status)
#admin.site.register(P)
#admin.site.register(Submission)


class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = (
        "id",
        "user",
        "sub_category",
        "title",
        "finished_at",
        #"sub_category__category__name",
        "status",
        "state",
        "display",
        "bids",
    )

    list_display_links = ("id","sub_category","title",)
    list_filter = ("sub_category__category__name","state","display")
    search_fields = ('id',"sub_category__category__name","sub_category__name",)
    list_editable = (
        "state",
        #"status",
        "display",
        "finished_at",
    )
    
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:     
            qs = self.model.objects.filter(user=request.user)#_default_manager.get_queryset()  
              
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



class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "proof",
        "status",
        "feedback",

    )

    list_display_links = ("id","job")
    list_filter = ("user","status","job__title","feedback")
    search_fields = ("user","status","job__title","feedback")
    list_editable = (
        "status",
        "feedback",
    )
    
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """      
        if request.user.is_superuser:
            qs = self.model._default_manager.get_queryset()
        else:                  
            qs = self.model.objects.filter(job__user=request.user)  
              
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs 
              
admin.site.register(Submission, SubmissionAdmin)

class BidAdmin(admin.ModelAdmin):
    form = BidForm
    list_display = (
        "id",
        "user",
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
    list_filter = ("id","job__title","user__username","user__profile__rating","user__profile__jobs_in_revision","user__profile__job_in_progress")
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
            qs = self.model.objects.filter(job__user=request.user) | self.model.objects.filter(bidder=request.user)
            
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



