from django.urls import path
from . import views

# Имя, которое позволяет именовать URL-адрес в масштабе всего проекта
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # используется конвертор путей
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name="post_detail")
]