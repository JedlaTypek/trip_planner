from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='index'),
    path('tag/<slug:slug>/', views.place_list_by_tag, name='place_list_by_tag'),

]
