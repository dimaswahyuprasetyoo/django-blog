from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/reply/', views.reply_to_comment, name='reply_to_comment'),
    
    # NEW: Reaction Path
    path('comment/<int:pk>/react/<str:reaction_type>/', views.react_to_comment, name='react_to_comment'),
]