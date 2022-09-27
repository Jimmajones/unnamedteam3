from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.get_register, name="register"),
    path("profiles/", views.get_profiles, name="profiles"),
    path("dashboard/<int:profile_id>", views.get_dashboard, name="dashboard"),
    path("detailed_view/<int:pokemon_id>/", views.get_detailed_view, name="detailed"),
    path("edit_pokemon/<int:pokemon_id>/", views.get_edit_pokemon, name="edit_pokemon"),
    path("create_pokemon/<int:profile_id>", views.get_create_pokemon, name="create_pokemon" ),
    path('new_location/<str:profile_id>', views.new_location, name="new_location"),
    path('new_move/<str:profile_id>', views.new_move, name="new_location"),
    path('new_ability/<str:profile_id>', views.new_ability, name="new_location"),
]