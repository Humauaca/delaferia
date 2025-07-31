from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from item import models
from . import forms
from django.views.generic.list import ListView


# Create your views here.
class HomePageView(ListView):
    model = models.Item
    template_name = 'core/index.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        return models.Item.objects.filter(quantity_in_stock__gt=0).order_by('-created_at')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        return context


def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = forms.SignupForm()

    return render(request, "core/signup.html", {
        'form': form
    })