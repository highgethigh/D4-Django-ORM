from django.urls import path
# импортируем наше представление
from .views import PostList, PostDetail, PostCreateView, PostDeleteView, PostUpdateView
from . import views

urlpatterns = [
    # # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post'),  # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
    path('search/', views.search, name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'), # ссылка на создание новости/статьи
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
]


