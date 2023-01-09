from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


MAX_LENGTH_TEXT = 1500


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=200,
        choices=ROLES,
        default=USER
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ["id"]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Categories(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=False
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.slug


class Genres(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=False
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["id"]


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False
    )
    year = models.IntegerField()
    description = models.CharField(
        max_length=1000,
        blank=False
    )
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genres
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Review(models.Model):
    CHOICES = [(x, str(x)) for x in range(1, 11)]
    text = models.CharField(max_length=MAX_LENGTH_TEXT,)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    pub_date = models.DateTimeField(auto_now_add=True,)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["title", "author"],
                                    name="unique_review"),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=MAX_LENGTH_TEXT)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(auto_now_add=True, )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
