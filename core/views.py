from django.shortcuts import redirect, render
from item import models
from . import forms
# Create your views here.
def index(request):
    """
    Render the index page.
    """
    items = models.Item.objects.filter(quantity_in_stock__gt=0)[:10]
    categories = models.Category.objects.all()
    return render(request, 'core/index.html', {'items': items, 
                                               'categories': categories})

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = forms.SignupForm()

    return render(request, "core/signup.html", {
        'form': form
    })