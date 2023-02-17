# D4-Django-ORM

Install using pip:
```
    pip3 install django-filter
```

Then add <b>'django_filters'</b> to your <b>INSTALLED_APPS</b>.
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




