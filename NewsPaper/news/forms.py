from django.forms import ModelForm, BooleanField
from .models import Post


# создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Галочка')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post  # это модель, по которой будет строиться форма

        # поля, которые будут выводиться на страничке
        fields = ['title', 'post_link_author', 'post_link_category', 'categoryType', 'text', 'check_box']