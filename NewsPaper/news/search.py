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

        # либо fields = [ 'title', 'post_data', 'post_link_author', 'text']
        # способ легче, без указаний значений ['icontains'], ['gt'], ['exact'], ['icontains'],

        