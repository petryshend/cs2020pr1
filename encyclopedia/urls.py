from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/search/', views.search_entry, name='search_entry'),
    path('wiki/<str:entry_name>/', views.view_entry, name='view_entry')
]
