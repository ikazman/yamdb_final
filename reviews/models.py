from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            verbose_name='Название жанра',
                            unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            verbose_name='Название объекта')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year)
        ]
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория объекта',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр объекта',
        blank=True,
        related_name='titles'
    )
    description = models.CharField(max_length=280, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    title = models.ForeignKey(
        Title,
        db_index=True,
        verbose_name='Название объекта',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews')
    score = models.PositiveIntegerField(
        null=True,
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария', blank=False)
    review = models.ForeignKey(
        Review,
        db_index=True,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    db_index=True,
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
