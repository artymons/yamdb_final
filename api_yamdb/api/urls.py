from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
    register,
    ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="review",
)

router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router.register("users", UserViewSet)
router.register("categories", CategoriesViewSet)
router.register("genres", GenresViewSet)
router.register("titles", TitleViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", register, name="register"),
    path("v1/auth/token/", get_token, name="token")
]
