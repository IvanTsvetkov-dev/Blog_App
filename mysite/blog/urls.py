from django.urls import path
from . import views

# Имя, которое позволяет именовать URL-адрес в масштабе всего проекта
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    # используется конвертор путей
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name="post_detail"),
    
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    
    path('<int:post_id>/comment/', views.post_comment, name='post_comment')
]