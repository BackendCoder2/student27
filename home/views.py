from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import  ContactUsForm
from users.models import User
from .models import UserStat,Index
from accounts.models import  Transaction,Account
from  datetime import date

def contact(request): 
    if request.method == "POST":
        cont_form = ContactUsForm(request.POST)
        if cont_form.is_valid():
            cont_form = cont_form.save(commit=False)
            if request.user.is_authenticated:
                cont_form.cmail = request.user.username 

            cont_form.save()
            return redirect('/')


    return render(request, 'home/contact.html')


#def index(request):
 #   return render(request, 'home/index.html')


def index(request,*args,**kwargs): 
    index=Index.objects.get(id=1)
    context = {"user": request.user,"index":index}
    return  render(request, 'home/index.html',context)
    


def affiliate(request):
    return render(request, 'home/affiliate.html')
        
def faqs(request):
    return render(request, 'home/faqs.html') 
   
          
@login_required(login_url="/users/login")    
def dashboard(request):
    wallet=Account.objects.get(user=request.user)
   # trans=Transaction.objects.filter(account=wallet)[:10]
    #transr=trans[:5]
    context = {"user": request.user,}
    
    return render(request, 'home/dashboard.html',context)    
        
    
