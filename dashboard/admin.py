from django.contrib import admin
from .models import Category,SubCategory,Job,Submission,Status,Type

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Type)
admin.site.register(Status)
#admin.site.register(Job)
#admin.site.register(Submission)


class JobAdmin(admin.ModelAdmin):
    #form = PersonForm
    list_display = (
        "id",
        "user",
        "sub_category",
        "title",
        "start_date",
        "end_date",
        #"sub_category__category__name",
        "closed",
        "approved",
    )

   # list_display_links = ("id","sub_category")
    list_filter = ("start_date","end_date","sub_category__category__name","closed","approved")
    search_fields = ("sub_category__category__name","sub_category__name","first_name","middle_name","last_name")
    list_editable = (
        "closed",
        "approved",
        "start_date",
        "end_date"
    )
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
admin.site.register(Submission, SubmissionAdmin)
