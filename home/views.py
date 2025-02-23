from django.shortcuts import render

def home(request, group_name):
    return render(request, 'index.html', {'group_name': group_name})