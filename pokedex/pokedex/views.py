from django.shortcuts import render
from django.http import HttpResponse

def get_dashboard(req):
    return render(req, 'dashboard.html')