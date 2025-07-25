from django.shortcuts import render
from item.models import Item
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required # type: ignore
def index(request):
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
        'title': 'Panel',
    })






