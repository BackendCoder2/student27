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



def index(request,*args,**kwargs): 
    index=Index.objects.get(id=1)
    context = {"user": request.user,"index":index}
    return  render(request, 'home/index.html',context)

