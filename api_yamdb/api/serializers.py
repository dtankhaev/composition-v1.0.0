import datetime as dt

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import UnicodeUsernameValidator

User = get_user_model()
username_validator = UnicodeUsernameValidator()


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[username_validator])

    class Meta:
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        if (
            User.objects.filter(username=value).exists()
            and not User.objects.filter(
                email=self.initial_data.get('email')
            ).exists()
        ):
            raise serializers.ValidationError('username занят.')
        return value

    def validate_email(self, email):
        if (
            not User.objects.filter(
                username=self.initial_data.get('username')
            ).exists()
            and User.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError('email занят.')
        return email


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class ShowTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""

    category = CatSerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('__all__')
        model = Title


class CreateTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        fields = ('__all__')
        model = Title

    def validate_year(self, value):
        """Валидатор для поля year.
        Год выпуска не может быть больше текущего.
        """
        year = dt.date.today().year
        if (year < value):
            raise serializers.ValidationError('Год выпуска не может быть '
                                              'больше текущего.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(f'Вы уже оставляли отзыв '
                                              f'к данному '
                                              f'произведению - {title.name}. '
                                              f'с id {title.id}')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор Me."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        read_only_fields = ('role', )
