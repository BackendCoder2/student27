from paypal.standard.forms import PayPalPaymentsForm
from django.conf import  settings
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import (
    CashWithrawal,
    Account,
    AccountSetting,
    CashDeposit,
    Currency
)
from .forms import (
    CashWithrawalForm,
)
from users.models import User
from mpesa_api.core.mpesa import Mpesa
import logging

logger = logging.getLogger(__name__)

@login_required(login_url="/user/login")
def mpesa_deposit(request):
    mssg = ""
    if request.method == "POST":
        phone_number = request.user.phone_number
        amount = request.POST.get("amount")
        #account=Account.ojects.get(user=request.user)
        try:
            Mpesa.stk_push(
                phone_number,
                amount,
                account_reference=f"{phone_number}",
                is_paybill=False,
            )           
            mssg=f"You should receive a prompt on your phone({phone_number}) shortly to enter MPESA PIN to complete deposit of KES {amount}."
        except Exception  as e:
            logger.exception(e)
            mssg="There is a problem making this deposit.Try again if you dont get a prompt in your phone to enter MPESA PIN"
            pass           
            
        #return redirect("/accounts/mpesa/deposit")  
       
   # trans_logz = CashDeposit.objects.filter(user=request.user).order_by("-id")[:10] 

    return render(
        request,
        "accounts/mp_deposit.html",
        {"mssg": mssg,}
    )
    

@login_required(login_url="/user/login")
def mpesa_withrawal(request):
    uf = Account.objects.get(user=request.user)
    try:
        currency=Currency.objects.get(name="KSH")
    except Currency.DoesNotExist:
        Currency.objects.create(name="KSH",rate=1) ###
        currency=Currency.objects.get(name="KSH")
    form = CashWithrawalForm()
    account=Account.objects.get(user=request.user)
    if request.method == "POST":
        data = {}
        data["account"] = account
        data["amount"] = request.POST.get("amount")
        data["withr_type"] = 'mpesa'
        data["currency"] = currency
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("/accounts/all_withrawal")#
       
    #trans_logz = CashWithrawal.objects.filter(user=request.user,withr_type='mpesa').order_by("-id")[:10]

    return render(
        request,
        "accounts/mpesa_withrawal.html",
        {"form": form,},
        #{"form": form, "trans_logz": trans_logz,"uf": uf},
    )
    



def format_mobile_no(mobile):
    mobile = str(mobile)
    if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
        return "254" + mobile[1:]
    if mobile.startswith("254") and len(mobile) == 12:
        return mobile
    if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
        return "254" + mobile
    return mobile


