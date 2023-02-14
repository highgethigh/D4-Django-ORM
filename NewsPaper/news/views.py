# импортируем класс "дженерик"
# который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
# импортируем модель пост
from .models import Post
from datetime import datetime
# импортируем класс "paginator"
from django.core.paginator import Paginator

# Create your views here.

# создадим модель объектов, которые будем выводить
class PostList(ListView):
    # название модели из файла models.py
    model = Post # модель Post
    # ссылка на шаблон странички, в данном случае файл templates/news.html
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')  # новости выводятся от старой до самой новой
    paginate_by = 10 # устанавливаем пагинацию на последние добавленные 10 новостей/статей
# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получить детали конкретно отдельного поста
    template_name = 'post.html'  # название шаблона будет news.html
    context_object_name = 'post'  # название объекта



