from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.get_main, name='main'),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    path('detailed_view/<str:id>/', views.get_detailed_view, name="detailed")
]