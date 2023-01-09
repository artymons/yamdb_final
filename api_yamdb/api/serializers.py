import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import (
    User,
    Categories,
    Genres,
    Title,
    Review,
    Comment,
)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = (
            'name',
            'slug'
        )


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = (
            'name',
            'slug'
        )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(
        many=True,
        read_only=True
    )
    category = CategoriesSerializer(
        many=False,
        read_only=True
    )
    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all(),
        required=True
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if (value > year):
            raise serializers.ValidationError(
                'Произведения из будущего не принимаются(')
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not data['username']:
            raise serializers.ValidationError('Username is required')
        user = get_object_or_404(
            User,
            username=self.initial_data.get("username")
        )
        if not default_token_generator.check_token(
                user,
                data['confirmation_code']
        ):
            raise serializers.ValidationError("Token incorrect")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    pub_date = serializers.DateTimeField(read_only=True,)

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        score = data["score"]

        if request.method == "POST":
            if Review.objects.filter(
                    title=title, author=request.user
            ).exists() and 10 >= score >= 1:
                raise ValidationError("Only one review is allowed")
        return data

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date",)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    pub_date = serializers.DateTimeField(read_only=True,)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date",)
