from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
@login_required 
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('item:detail')
    
    conversations = models.Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass # redirect to the existing conversation

    if request.method == "POST":
        form = forms.ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = models.Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    
    else:
        form = forms.ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form,
    })

@never_cache
@login_required
def inbox(request):
    conversations = models.Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })

@never_cache
@login_required
def detail(request, pk):
    conversation = models.Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = forms.ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = forms.ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })