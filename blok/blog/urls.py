from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from blog.views import PostViewSet, CommentViewSet  # Импортируем представления

# Создаем основной маршрутизатор для Post
router = DefaultRouter()
router.register(r'posts', PostViewSet)

# Создаем вложенный маршрутизатор для Comment
posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты для Post
    path('posts/', include(posts_router.urls)),  # Включаем маршруты для Comment, добавлен путь 'posts/'
]
