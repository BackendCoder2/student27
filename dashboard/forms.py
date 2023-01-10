from django import forms
from .models import Job,Bid

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ("user","assigned_to","status","employer")
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ("user","bidder")        

