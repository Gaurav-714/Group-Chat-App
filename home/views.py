from django.shortcuts import render
from .models import ChatModel, GroupModel

def home(request, group_name):
    group_obj = GroupModel.objects.filter(name=group_name).first()
    if not group_obj and group_name != 'favicon.ico':
        GroupModel.objects.create(name=group_name)

    chats = []
    chats = ChatModel.objects.filter(group=group_obj)

    context = {
        'group_name': group_name,
        'chats': chats
    }
    return render(request, 'index.html', context)