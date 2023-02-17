# D4-Django-ORM

Установить джанго-фильтры через pip:
```
    pip3 install django-filter
```

Добавить <b>'django_filters'</b> в  <b>INSTALLED_APPS</b>.
```
    INSTALLED_APPS = [
    ...
    'django_filters',
]
```
Создаем файл <b>search.py</b> для фильтров
```
    from django_filters import FilterSet
    from .models import Post

    class PostFilter(FilterSet):
        class Meta:
            model = Post
            fields = {
                # по названию заголовка
                'title': ['icontains'],
                # позже какой-либо даты
                'post_data': ['gt'],
                # по имени пользователя автора
                'post_link_author': ['exact'], # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь

                'text': ['icontains'],
            }
```

Создаем новую вьюшку для фильтров в папке views.py:
```
    from django.shortcuts import render
    from .search import PostFilter
    def search(request):
        listings = Post.objects.all()
        listing_filter = PostFilter(request.GET, queryset=listings)
        context = {
            'listing_filter': listing_filter,
        }
        return render(request, "search.html", context)
```

В приложение news в урлах добавил страничку для news/search
```
    from . import views
    path('search/', views.search, name='search'),
```

ПАГИНАЦИЯ во views.py в классе PostList устанавливаем вывод 10 новостей/статей на одной странице при помощи команды <b>paginate_by</b>:
```
    paginate_by = 10 # устанавливаем пагинацию на последние добавленные 10 новостей/статей
```
В HTML с новостями устанавливаем навигацию по новостям::
```
    <!-- Проверяем что поддерживается постраничный вывод -->
    {% if is_paginated %}
    <div align="center">
        Всего новостей на этой старанице: {{ news | length }}
        <br>
        страница {{ page_obj.number}} из {{ page_obj.paginator.num_pages }} страниц
        <br>
        {% if page_obj.has_previous %}
            <a href="?page=1">First</a>
            <a href="?page={{ page_obj.previous_page_number }}"><<<</a>
        {% endif %}
        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
                <a>{{ num }}</a>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <a href="?page={{ num }}">{{ num }}</a>
            {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">>>></a>
            <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
        {% endif %}
    </div>
    {% endif%}
```