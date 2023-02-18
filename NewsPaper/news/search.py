from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = [ 'title', 'post_data', 'post_link_author', 'categoryType', 'text']



        # либо fields = [ 'title', 'post_data', 'post_link_author', 'categoryType', 'text']
        # способ легче, без указаний значений ['icontains'], ['gt'], ['exact'], ['icontains'],

        # fields = {
            # по названию заголовка
#           'title': ['icontains'],
#           # позже какой-либо даты
#           'post_data': ['gt'],
#           # по имени пользователя автора
#           'post_link_author': ['exact'], # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
#
#           'categoryType': ['exact'],
#
#           'text': ['icontains'],
#        }