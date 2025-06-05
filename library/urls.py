from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/', views.place_list, name='places'),
    path('tag/list/<slug:slug>/', views.place_list_by_tag, name='place_list_by_tag'),
    path('place/detail/<slug:slug>/', views.place_detail, name='place_detail'),
    path('place/add/', views.place_add, name='place_add'),
    path('place/delete/<slug:slug>/', views.PlaceDeleteView.as_view(), name='place_delete'),
    path('place/edit/<slug:slug>/', views.place_edit, name='place_edit'),
    path('trips/', views.trip_list, name='trips'),
    path('trip/add/', views.trip_add, name='trip_add'),
    path('trip/delete/<slug:slug>/', views.TripDeleteView.as_view(), name='trip_delete'),
    path('trip/edit/<slug:slug>/', views.trip_edit, name='trip_edit'),
    path('trip/detail/<slug:slug>/', views.trip_detail, name='trip_detail'),
]
