from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework_simplejwt.tokens import RefreshToken

class BlogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        # Создаём тестовый пост
        self.post = Post.objects.create(title='Test Post', content='Post content', author=self.user)

    def test_create_post(self):
        data = {'title': 'New Post', 'content': 'Content of new post'}
        response = self.client.post('/api/posts/', data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_post_by_title(self):
        response = self.client.get('/api/posts/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Test' in post['title'] for post in response.data))

    def test_update_post(self):
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.put(f'/api/posts/{self.post.id}/', data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_comment(self):
        data = {'post': self.post.id, 'text': 'Nice post!', 'author': self.user.id}
        response = self.client.post('/api/comments/', data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_with_comments(self):
        Comment.objects.create(post=self.post, text='Great!', author=self.user)
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comments', response.data)
