# импортируем класс "дженерик"
# который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импортируем модель пост
from .models import Post
from datetime import datetime
# импортируем класс "paginator"
from django.core.paginator import Paginator
from .forms import PostForm


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

    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# создаём представление, в котором будут детали конкретной отдельной новости/статьи
class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получить детали конкретно отдельного поста
    template_name = 'post.html'  # название шаблона будет post.html
    context_object_name = 'post'  # название объекта


from django.shortcuts import render
from .search import PostFilter
def search(request):
    listings = Post.objects.all()
    listing_filter = PostFilter(request.GET, queryset=listings)
    context = {
        'listing_filter': listing_filter,
    }
    return render(request, "search.html", context)



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

