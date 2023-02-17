from django.urls import path
# импортируем наше представление
from .views import PostList, PostDetail
from . import views

urlpatterns = [
    # # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post'),  # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
    path('search/', views.search, name='search'),
]


