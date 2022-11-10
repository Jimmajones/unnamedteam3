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
    path("new_location/<int:profile_id>", views.new_location, name="new_location"),
    path("new_move/<int:profile_id>", views.new_move, name="new_move"),
    path("new_ability/<int:profile_id>", views.new_ability, name="new_ability"),
    path("delete_pokemon/<int:pokemon_id>/", views.delete_pokemon, name="delete_pokemon"),
    path("delete_locations/<int:pokemon_id>/", views.delete_locations, name="delete_locations"),
    path("delete_moves/<int:pokemon_id>/", views.delete_moves, name="delete_moves"),
    path("delete_abilities/<int:pokemon_id>/", views.delete_moves, name="delete_abilities"),
    path("delete_profile/<int:profile_id>/", views.delete_profile, name = "delete_profile"),
]