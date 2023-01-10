from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Job,Bid,Submission
#from paypal.models import UserFund
from django.views.decorators.csrf import csrf_exempt

import os
import pathlib
#from authentication.models import Profile
from django.contrib.auth.decorators import login_required



@login_required(login_url="/users/login/")
def post_job(request):
    if request.method == "POST":
        uf = UserFund.objects.get(user=request.user)
        if uf.fund < float(request.POST["price"]) * int(request.POST["quantity"]) and not request.user.is_trusted:
            return HttpResponse("Please deposit more money")#redirect/deposit_fund_pa
        Job(user=request.user, title=request.POST["title"], description=request.POST["description"], price=float(request.POST["price"]), quantity=int(request.POST["quantity"])).save()
        return redirect("/")
    return render(request, "dashboard/post-job.html")
    
    
    
    

@login_required(login_url="/users/login/")
def view_task(request, task_id):
    task = Job.objects.get(id=task_id)

    try:
        s = Submission.objects.get(job=task, user=request.user)
        if s.status == "revise":
            return render(request, "dashboard/task.html", {
                "task": task,
                "submission": s
            })
        return HttpResponse("You already submitted a proof, please wait employer to send you a response back. ")
    except Submission.DoesNotExist:
        pass

    if request.method == "POST":
        try:
            s = Submission(user=request.user, job=task, status="revise")
            s.proof = request.POST["proof"]
            s.save()
        except Submission.DoesNotExist:
            Submission(user=request.user, job=task, proof=request.POST["proof"]).save()
        return HttpResponse("Proof submitted successfully. If you don't hear a response back within a week, your submission will automatically approved")

    else:
        return render(request, "dashboard/task.html", {
            "task": task
        })


@login_required(login_url="/users/login/")
def jobs_submitted_tasker(request):
    tasks = Submission.objects.filter(user=request.user)
    return render(request, "dashboard/job-submitted-dashboard.html", {
        "tasks": tasks
    })

@login_required(login_url="/users/login/")
def cancel_job(request, job_id):
    job = Job.objects.get(id=job_id)
    task = Submission.objects.get(user=request.user, job=job)
    task.delete()
    return redirect("/tasks/")

@login_required(login_url="/users/login/")
def employer_dashboard(request):
    jobs = Job.objects.filter(user=request.user)
    submissions = []
    for job in jobs:
        submissions.append(Submission.objects.filter(job=job))
    return render(request, "dashboard/employer-dashboard.html", {
        "submissions": submissions
    })

@login_required(login_url="/users/login/")
def review_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
   # profile = Profile.objects.get(user=submission.user)
    return render(request, "dashboard/submission.html", {
        "submission": submission,
       # "profile": profile
    })

@login_required(login_url="/users/login/")
def employer_submission_failed(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "failed"
    submission.save()
    return redirect("/employer-dashboard/")

@login_required(login_url="/users/login/")
def employer_submission_revise(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "revise"
    submission.save()
    return redirect("/employer-dashboard/")

@login_required(login_url="/users/login/")
def employer_submission_success(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "success"
    submission.save()

    worker_fund = UserFund.objects.get(user=submission.user)
    employer_fund = UserFund.objects.get(user=submission.job.user)
    price = submission.job.price

    worker_fund.fund += price
    employer_fund.fund -= price
    worker_fund.save()
    employer_fund.save()

    return redirect("/employer-dashboard/")
    
    
#-------------------------------------------------------------    
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Job


@login_required(login_url="/users/login/")
def index(request):
    jobs = Job.objects.all()
    return render(request, "dashboard/new/index.html", {
        "jobs": jobs
    })

class JobListView(ListView):
    #queryset = Job.objects.filter(status='AV',display=True)
    context_object_name = 'job_list'
    template_name = 'dashboard/new/job_list.html'
    
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="AV")
        return Job.objects.filter(status='AV',display=True)
        
class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'dashboard/new/job_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()        
        print("CONTEST",context)     
        return context 

class BidListView(ListView):   
    context_object_name = 'bid_list'
    #paginate_by = 100  # if pagination is desired
    template_name = 'dashboard/new/bid_list.html'   
    
    #model = Bid
    #queryset = Bid.objects.filter(job__id=1)
    def get_queryset(self):
        return Bid.objects.filter(bidder=self.request.user,job__status="AV") 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context 

class JobInProgressListView(ListView):

    context_object_name = 'job_in_progress_list'
    template_name = 'dashboard/new/jobs_in_progress.html'
    
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="PR")
        return Job.objects.filter(assigned_to=self.request.user,status="PR")       
        
            

class JobInReviewListView(ListView):

    context_object_name = 'job_in_review_list'
    template_name = 'dashboard/new/jobs_in_review.html'
    
          
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="RW")
        return Job.objects.filter(assigned_to=self.request.user,status="RW")
        
        
class JobInRevisionListView(ListView):

    context_object_name = 'job_in_revision_list'
    template_name = 'dashboard/new/jobs_in_revision.html'
    
 
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="RV")
        return Job.objects.filter(assigned_to=self.request.user,status="RV")        
        
class JobClosedListView(ListView):

    context_object_name = 'job_closed_list'
    template_name = 'dashboard/new/jobs_closed.html'
    
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="CL")
        return Job.objects.filter(assigned_to=self.request.user,status="CL")        
        
