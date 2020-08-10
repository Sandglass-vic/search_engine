from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search_view, name='search_view'),
    path('search/?keyword=<keyword>', views.search, name='search'),
    path('search/detail/<news_id>', views.detail, name='detail'),
]