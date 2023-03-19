from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CatViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
                       TitleViewSet, TokenViewAPI, UserViewSet, signup_post)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CatViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UserViewSet, basename='users')
registration = [
    path('auth/signup/', signup_post),
    path('auth/token/', TokenViewAPI.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(registration))
]
