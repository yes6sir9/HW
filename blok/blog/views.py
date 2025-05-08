from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import filters

# Представление для работы с постами (CRUD для Post)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # Получаем все посты
    serializer_class = PostSerializer  # Используем сериализатор PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # Права доступа
    filter_backends = (filters.SearchFilter,)  # Добавляем фильтрацию
    search_fields = ['title']  # Фильтрация по полю title

    def perform_create(self, serializer):
        # Сохраняем пост, устанавливая текущего пользователя как автора
        serializer.save(author=self.request.user)

# Представление для работы с комментариями (CRUD для Comment)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer  # Используем сериализатор CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # Права доступа

    def get_queryset(self):
        # Фильтруем комментарии по посту (используем post_pk для получения комментариев к конкретному посту)
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        # Сохраняем комментарий, устанавливая текущего пользователя как автора и post_id как соответствующий пост
        serializer.save(author=self.request.user, post_id=self.kwargs['post_pk'])
