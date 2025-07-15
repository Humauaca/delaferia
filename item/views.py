from django.shortcuts import render, redirect, get_object_or_404
from item import models
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms
from django.db.models import Q
from django.views.decorators.cache import never_cache

# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    category_id =request.GET.get('category', 0)
    categories = models.Category.objects.all()
    items = models.Item.objects.filter(quantity_in_stock__gt=0)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'title': 'Productos Disponibles',
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    related_items = models.Item.objects.filter(category=item.category).exclude(pk=item.pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
    })


@user_passes_test(lambda u: u.is_staff)
@never_cache
@login_required # type: ignore
def newItem(request):
    if request.method == 'POST':
        form = forms.NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = forms.NewItemForm()
    
    return render(request, 'item/new_item.html', {
        'form': form,
        'title': 'Nuevo Producto',
    })

@never_cache
@login_required # type: ignore
def editItem(request, pk):
    item = get_object_or_404(models.Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form =forms.EditItemForm(request.POST, request.FILES, instance=item) # instance=item

        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id) # type: ignore
        
    else:
        form = forms.EditItemForm(instance=item)

    return render(request, 'item/new_item.html', {
        'form': form,
        'title': 'Editar Producto',
    })

@never_cache
@login_required # type: ignore
def delete(request, pk):
    item = get_object_or_404(models.Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
