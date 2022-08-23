from django.shortcuts import render

# Create your views here.
def get_main(req):
    return render(req, 'main.html')

def get_dashboard(req):
    return render(req, 'dashboard.html')
