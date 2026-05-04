from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Comment


class PostModelTest(TestCase):
    def test_post_creation(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(str(post), "Test Post")

    def test_comment_creation(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        self.assertEqual(comment.author, "Author")
        self.assertEqual(str(comment), "Comment by Author on Test Post")


class BlogViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/index.html")

    def test_post_detail_view(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        response = self.client.get(reverse('post_detail', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
        self.assertContains(response, "Test Post")

    def test_add_comment_view_get(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        response = self.client.get(reverse('add_comment', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/add_comment.html")

    def test_add_comment_view_post(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        response = self.client.post(
            reverse('add_comment', args=[post.id]),
            {"author": "Test Author", "text": "Test Comment"},
        )
        self.assertRedirects(response, reverse('post_detail', args=[post.id]))
        self.assertEqual(Comment.objects.count(), 1)

    def test_edit_comment_view_get(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        response = self.client.get(reverse('edit_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/edit_comment.html")

    def test_edit_comment_view_post(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        response = self.client.post(
            reverse('edit_comment', args=[comment.id]),
            {"author": "Updated Author", "text": "Updated Comment"},
        )
        self.assertRedirects(response, reverse('post_detail', args=[post.id]))
        comment.refresh_from_db()
        self.assertEqual(comment.author, "Updated Author")

    def test_delete_comment_view_get(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        response = self.client.get(reverse('delete_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/delete_comment.html")

    def test_delete_comment_view_post(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        response = self.client.post(reverse('delete_comment', args=[comment.id]))
        self.assertRedirects(response, reverse('post_detail', args=[post.id]))
        self.assertEqual(Comment.objects.count(), 0)

    def test_pagination(self):
        for i in range(10):
            Post.objects.create(title=f"Test Post {i}", content="Test Content")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pagination")

    def test_empty_fields_add_comment(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        response = self.client.post(
            reverse('add_comment', args=[post.id]), {"author": "", "text": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fill in all fields.")

    def test_empty_fields_edit_comment(self):
        post = Post.objects.create(title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, author="Author", text="Comment")
        response = self.client.post(
            reverse('edit_comment', args=[comment.id]), {"author": "", "text": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fill in all fields.")
