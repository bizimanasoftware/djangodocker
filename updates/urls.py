# updates/urls.py

from django.urls import path
from . import views

app_name = 'updates'

urlpatterns = [
    # Public URLs
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='post_list_by_category'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Admin Management URLs
    path('manage/', views.AdminPostListView.as_view(), name='admin_post_list'),
    path('manage/new/', views.PostCreateView.as_view(), name='post_create'),
    path('manage/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('manage/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
