from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Job,Bid,Submission
#from paypal.models import UserFund
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

    
#------------------------------------------------------------- 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from .models import Job,DFile,Bid,Submission


@login_required(login_url="/users/login/")
def index(request):
    job=Job.objects
    
    if not request.user.is_employer:
        t_count = job.count()
        av_count = job.filter(status="AV").count
        closed= job.filter(assigned_to=request.user,status="CL").count
        active=job.filter(user=request.user,status="PR").count
        bids=Bid.objects.filter(bidder=request.user).count
        if t_count==0:
            t_count=1 
        per_done=round((job.filter(assigned_to=request.user,status="CL").count()/t_count)*100,1)
    else:
        t_count = job.filter(employer=request.user).count()
        av_count = job.filter(status="AV",employer=request.user).count
        closed= job.filter(assigned_to=request.user,status="CL").count
        active=job.filter(user=request.user,status="PR").count
        bids=Bid.objects.filter(bidder=request.user).count
        if t_count==0:
            t_count=1 
        per_done=round((job.filter(assigned_to=request.user,status="CL").count()/t_count)*100 ,1)   
    
    
    
    
    context={"av_count":av_count,"t_count":t_count,"closed":closed,"active":active,"bids":bids,"per_done":per_done}
    return render(request, "dashboard/new/index.html", context)

class JobListView(ListView):
    #queryset = Job.objects.filter(status='AV',display=True)
    context_object_name = 'job_list'
    template_name = 'dashboard/new/job_list.html'
    
    def get_queryset(self):         
        if self.request.user.is_employer:
            return Job.objects.filter(employer=self.request.user,status="AV")
        return Job.objects.filter(status='AV',display=True)
        
class JobDetailView(DetailView):
    #model = Job
    context_object_name = 'job'
    template_name = 'dashboard/new/job_detail.html'
    
    def get_queryset(self):         
        self.user=self.request.user
        return Job.objects.all()        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       # context['now'] = timezone.now()
        #print('KK',kwargs['object'].id)
        
        context['dfile'] = DFile.objects.filter(job__id=kwargs['object'].id)
        #context['rfile'] = RevInfo.objects.filter(job_id=kwargs['object'].id)

        context['rev_no'] =Submission.objects.filter(job_id=kwargs['object'].id).count
        
        context['submissions'] = Submission.objects.filter(job_id=kwargs['object'].id)
        
        context['bids']= Bid.objects.filter(job__id=kwargs['object'].id,bidder=self.user).count
        
        
    
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



class AcceptBidUpdateView(UpdateView):
     model = Bid
     fields = ['accept']
    # template_name_suffix = '_update_form_bid'
     template_name = 'dashboard/new/bid_update_form_bid.html'
     success_url = '/dashboard/job-in-progress/'
     
class JobUpdateView(UpdateView):
     model = Job
     fields = ['bids']
    # template_name_suffix = '_update_form_bid'
     template_name = 'dashboard/new/bid_update_form_bid.html'
     success_url = '/dashboard/job-in-progress/'
 
     
@login_required(login_url="/users/login/")
def cancel_bid(request, job_id):
    job = Job.objects.get(id=job_id)
    bid = Bid.objects.get(user=request.user, job=job)
    task.delete()
    return redirect("/dashboard/bid-list") 
    
    
    
@login_required(login_url="/users/login/")
def create_bid(request, *args, **kwargs): 
    print(args, kwargs)
    desrc = request.POST.get("description")
    job = Job.objects.get(id=kwargs['pk']) 
    #Bid.objects.create(user=request.user,description=desrc, job=job)
    return redirect('/dashboard/bid-list/')
    
    


####BUTTONS##
#W
@login_required(login_url="/users/login/")
def bid(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    desrc = request.POST.get("description")
    Bid.objects.create(user=request.user,description=desrc, job=job)
    return redirect('/dashboard/bid-list/')

#EW
@login_required(login_url="/users/login/")
def delete_bid(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if not request.user.is_employer:
        bids=Bid.objects.filter(user=request.user, job_id=job.id)
        bids.delete()
        return redirect('/dashboard/bid-list/')
        
    bids=Bid.objects.filter(job__employer=request.user, job_id=job.id) 
    bids.delete()
    return redirect(f'/dashboard/job-list/{job_id}/bid-list/')

#W    
@login_required(login_url="/users/login/")    
def accept_bid(request, bid_id):
    bid=Bid.objects.get(id=bid_id)
    bid.accept=True
    bid.save()
    
    return redirect('/dashboard/job-in-progress/')

#E
@login_required(login_url="/users/login/")    
def approve_bid(request, bid_id):
    bid=Bid.objects.get(id=bid_id)
    bid.approve=True
    bid.save()
    return redirect(f'/dashboard/job-list/{bid.job.id}/bid-list/')    
    
#E    
@login_required(login_url="/users/login/")
def bid_list_per_job(request,job_id):
    job=Job.objects.get(id=job_id)
    bids = Bid.objects.filter(job_id=job_id)
    if  request.user.is_employer:
        return render(request, "dashboard/new/bid-list-user.html", {
        "bids": bids,"job":job })  
        
    return redirect('/dashboard/bid-list/')

#E

class CreateJobView(CreateView):
    model = Job
    fields = [
        "sub_category",
        "title",
        "description",
        "finished_at",
        "display",  
        ]
    template_name = 'dashboard/new/create_job.html'
    success_url = '/dashboard/job-list/'#W 
    
    
@login_required(login_url="/users/login/")    
def accept_job(request, job_id):
    job=Job.objects.get(id=job_id)
    job.accepted=True
    job.save()
    
    return redirect('/dashboard/job-closed/')
    
    
@login_required(login_url="/users/login/")
def create_submission(request,job_id):
    if request.method == "POST":
        job=Job.objects.get(id=job_id)
        
        Submission.objects.create(job=job,user=request.user)#, proof=request.POST["proof"])
        
        return redirect(f"/dashboard/job-list/{job_id}")


from .models import DFile
from .forms import DFileForm


def upload_file(request,job_id,sub_id):
    job=Job.objects.get(id=job_id)
    submission=Submission.objects.get(id=sub_id)
    if request.method == 'POST':
        newdoc = DFile(job=job,submission=submission,dfile=request.FILES['docfile'])
        newdoc.save()
        return redirect(f"/dashboard/job-list/{job_id}")
        
def submissione(request,job_id):
    job=Job.objects.get(id=job_id)
    
    if request.method == 'POST':
        proof = request.POST.get("proof")
       # final = request.POST.get("final")
        document=request.FILES['document']
        
        Submission.objects.create(job=job,proof=proof)
        return redirect(f"/dashboard/job-list/{job_id}")


    return render(request, "dashboard/new/submission.html",{"job_id":job_id})
    
from .forms import DocumentForm
    
def submission(request,job_id):
    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    job=Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Submission(job=job,document=request.FILES['document'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect(f"/dashboard/job-list/{job_id}/submission")
        else:
            message = 'The form is not valid. Fix the following error:'
            print(form.errors)
    else:
        form = DocumentForm()  # An empty, unbound form
        
       
    documents=Submission.objects.filter(job=job)
    return render(request, "dashboard/new/submission.html",{"job_id":job_id,"form":form,"documents":documents})
    
