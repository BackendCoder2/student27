from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Submission

class SubmissionCreateView(CreateView):
    model = Submission
    fields = ['job','proof','feedback','status']
    
   # def form_valid(self, form):
   #         form.instance.created_by = self.request.user
   #         return super().form_valid(form)
            
class SubmissionUpdateView(UpdateView):
    model = Submission
    fields = ['name']

class SubmissionDeleteView(DeleteView):
    model = Submission
    success_url = reverse_lazy('submission-list')
    

class SubmissionListView(ListView):
    model = Submission
    paginate_by = 100  # if pagination is desired
        
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['now'] = timezone.now()
    #    return context    
