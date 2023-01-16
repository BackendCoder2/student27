from django import forms
from .models import Job,Bid

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = (     
        "id",
        "order_id",
        "user",
        "assigned_to",
        "status",
        "employer",
        "bids", 
        "accepted",
        "rejected",
        "rejection_description",
        "rejected_work_accepted",
        "paid",
        "revise",
        )
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ("user","bidder")        


class DFileForm(forms.Form):
    dfile = forms.FileField(label='Select a file')
    
class DocumentForm(forms.Form):
    document = forms.FileField(label='Select a file')
