from django.urls import path
from . import views
from .gviews import SubmissionCreateView, SubmissionDeleteView, SubmissionUpdateView,SubmissionListView

#-----------
from .views import JobListView,JobDetailView,BidListView,JobInProgressListView,JobInReviewListView,JobInRevisionListView,JobClosedListView,AcceptBidUpdateView,CreateJobView

app_name = "dashboard"

urlpatterns = [
    
    path("post-job/", views.post_job),
    path("task/<int:task_id>/", views.view_task),
    #path("api/upload/", views.file_upload_backend),
    path("tasks/", views.jobs_submitted_tasker),
    path("tasker/job/cancel/<int:job_id>", views.cancel_job),
    path("employer-dashboard/", views.employer_dashboard),
    path("submission/<int:submission_id>", views.review_submission),
    path("submission/<int:submission_id>/failed/", views.employer_submission_failed),
    path("submission/<int:submission_id>/success/", views.employer_submission_success),
    path("submission/<int:submission_id>/revise/", views.employer_submission_revise),
    
    
    
    #path('submission/add/', SubmissionCreateView.as_view(), name='submission-add'),
    #path('submission/<int:pk>/', SubmissionUpdateView.as_view(), name='submission-update'),
    #path('submission/<int:pk>/delete/', SubmissionDeleteView.as_view(), name='submission-delete'),   
    #path('submission', SubmissionListView.as_view(), name='submission-list'), 
    
    #----------------
    
    path("", views.index),
    path('job-list/', JobListView.as_view(), name='job-list'),
    path('job-list/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('bid-list/', BidListView.as_view(), name='bid-list'),
    path('job-in-progress/', JobInProgressListView.as_view(), name='job-in-progress'),
    
    path('job-in-review/', JobInReviewListView.as_view(), name='job-in-review'),    
    path('jobs-in-revision/', JobInRevisionListView.as_view(), name='jobs-in-revision'),    
    path('job-closed/', JobClosedListView.as_view(), name='job-closed'),
    path('bid-accept/<int:pk>/', AcceptBidUpdateView.as_view(), name='bid-accept'),
    path("create-bid/", views.create_bid, name='create-bid'),
    path("create-bid/<int:pk>", views.create_bid, name='create-bid'),
    
    #E
    path("create-job/", CreateJobView.as_view(), name='create-job'),
    
    
    #buttons
    path('<int:job_id>/create-bid/', views.bid, name='bid'),
    path('<int:job_id>/delete-bid/', views.delete_bid, name='delete_bid'),
    path('<int:job_id>/accept-bid/', views.accept_bid, name='accept_bid'),
    
   ]
   

