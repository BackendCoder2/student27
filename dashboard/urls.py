from django.urls import path
from . import views

from .views import JobListView,JobDetailView,BidListView,JobInProgressListView,JobInReviewListView,JobInRevisionListView,JobClosedListView,AcceptBidUpdateView,CreateJobView

app_name = "dashboard"

urlpatterns = [

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
    path('<int:bid_id>/accept-bid/', views.accept_bid, name='accept-bid'),
    path('<int:bid_id>/approve-bid/', views.approve_bid, name='approve-bid'),
    path('job-list/<int:job_id>/bid-list/', views.bid_list_per_job, name='bid-list-per-job'),
    
   
    path('<int:job_id>/accept-job/', views.accept_job, name='accept-job'), #E
    
    path('<int:job_id>/create-submission/', views.create_submission, name='create-submission'), #E
    path('job-list/<int:job_id>/bid-list/<int:sub_id>/upload_file/', views.upload_file, name='upload_file'), #E
    
    
    
    path('job-list/<int:job_id>/submission/', views.submission, name='submission'), #E
   ]
   

