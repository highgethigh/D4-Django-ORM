from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, DateTimeField


# Create your models here.

# модель Author


class Author(models.Model):
    # Имеет следующие поля:
    # связь «один к одному» с встроенной моделью пользователей User
    authors_link_user = models.OneToOneField(User, on_delete=models.CASCADE)

    # рейтинг пользователя
    author_rating = models.FloatField(default=0)

    # метод update_rating,
    # который обновляет рейтинг пользователя, переданный в аргумент этого метода.
    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям автора
        postRat = self.post_set.all().aggregate(post_rating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('post_rating')

        # суммарный рейтинг всех комментариев автора
        commentRat = self.authors_link_user.comment_set.all().aggregate(comment_rating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('comment_rating')

        # суммарный рейтинг каждой статьи автора умножается на 3
        self.author_rating = pRat * 3 + cRat
        self.save()

    # в админке отображается название автора, а не Author.objects
    def __str__(self):
        return self.authors_link_user.username.title()
        
# модель Category
class Category(models.Model):
    # название категории новостей/статей их главная тематика
    name_category = models.CharField(max_length=55, unique=True)


# модель Post
class Post(models.Model):
    # связь «один ко многим» с моделью Author
    post_link_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # # варианты для поля с выбором (новость или статья)
    news = 'N'
    articles = 'A'

    CATEGORY_CHOICES = [
        (news, 'Новости'),
        (articles, 'Статьи')
    ]

    # поле тип категории
    categoryType = models.CharField(max_length=1,
                                    choices=CATEGORY_CHOICES,
                                    default=news)

    # автоматически добавляемая дата и время создания
    post_data: DateTimeField = models.DateTimeField(auto_now_add=True)  # дата создания объекта

    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory через through)
    post_link_category = models.ManyToManyField(Category, through='PostCategory')

    # заголовок статьи/новости
    title = models.CharField(max_length=255)

    # текст статьи/новости
    text = models.TextField()

    # рейтинг статьи/новости
    rating = models.FloatField(default=0)

    # метод like увеличивает рейтинг статьи/новости на единицу
    def like(self):
        self.rating += 1
        self.save()

    # метод dislike уменьшает рейтинг статьи/новости на единицу
    def dislike(self):
        self.rating -= 1
        self.save()

    # метод preview, который возвращает начало статьи
    # (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return self.title # в админке отображается название заголовка, а не Post.objects
# модель PostCategory
class PostCategory(models.Model):
    # Промежуточная модель для связи «многие ко многим»:
    # связь «один ко многим» с моделью Post
    postc_link_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» с моделью Category
    postc_link_category = models.ForeignKey(Category, on_delete=models.CASCADE)

# модель Comment


class Comment(models.Model):
    # Модель будет иметь следующие поля:
    # связь «один ко многим» с моделью Post
    comment_link_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» со встроенной
    # моделью User (комментарии может оставить любой пользователь, необязательно автор)
    comment_link_user = models.ForeignKey(User, on_delete=models.CASCADE)

    # текст комментария
    text_comment = models.TextField()

    # дата и время создания комментария
    create_data_comment = models.DateTimeField(auto_now_add=True)

    # рейтинг комментария
    rating = models.FloatField(max_length=20, default=0)

    # метод like увеличивает рейтинг комментария на единицу
    def like(self):
        self.rating += 1
        self.save()

    # метод dislike уменьшает рейтинг комментария на единицу
    def dislike(self):
        self.rating -= 1
        self.save()
