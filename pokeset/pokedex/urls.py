from django.urls import path

from . import views

urlpatterns = [
    path('',views.get_login, name = 'login'),
    path('login/', views.get_login, name = "login"),
    path('register/', views.get_register, name = "register"),
    path('main/', views.get_main, name='main'),
    path('profiles/', views.get_profiles, name = "profiles"),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    path('detailed_view/<str:id>/', views.get_detailed_view, name="detailed"),
    path('edit_pokemon/<str:id>/', views.get_edit_pokemon, name="edit")
]