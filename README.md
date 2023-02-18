# D4-Django-ORM
# Перед запуском проекта запустить виртуальное окружение через консоль:
```
    source venv/bin/activate
```
### Задание:
1. Усовершенствовать ваш новостной портал. Добавить постраничный вывод и отдельную страницу с поиском /search/, чтобы пользователь мог сортировать новости по дате и имени автора.
2. Необходимо иметь возможность создавать новые новости и статьи не только из админки, но и в самом приложении. Для такой возможности необходимо создать модельные формы.
3. Необходимо добавить на сайт с помощью дженериков новые страницы /news/add/, а также /news/<int:pk>/edit/. На этих страницах пользователь может добавить или редактировать новости.
4. Добавьте страницу удаления новостей /news/<int:pk>/delete/. На ней после подтверждения пользователь может удалить страницу с новостью.

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

Создаем файл <b>forms.py</b> в приложение
```
    from django.forms import ModelForm, BooleanField
    from .models import Post


    # создаём модельную форму
    class PostForm(ModelForm):
        check_box = BooleanField(label='Галочка')  # добавляем галочку, или же true-false поле

        class Meta:
            model = Post  # это модель, по которой будет строиться форма

            # поля, которые будут выводиться на страничке
            fields = ['title', 'post_link_author', 'post_link_category', 'categoryType', 'text', 'check_box']
```

В модели <b>POST</b> добавил инструкцию для перехода на новость/статью после её создания:
```
    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с этой новостью
        return f'/news/{self.id}'
```

Обновить пути в <b>urls.py</b> в самом приложение:
```
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
```


В файле <b>views.py</b> переходим в класс <b>PostList</b> добавляем метод и импортируем форму:
```
    from .forms import PostForm
    form = 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
```
Далее импортируем дженерики для создания, удаления и редактирования Постов и заготавливаем классы для этого:
```
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    

# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
```
Для отображения создаем для этого html-страницы: 
1. <b>post_create.html</b>
2. <b>post_delete.html</b>
3. <b>post_edit.html</b>