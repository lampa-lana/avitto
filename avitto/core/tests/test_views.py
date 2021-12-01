from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestCoreViews(TestCase):
    def setUp(self):
        client = Client()
        self.response = client.get('')
        super().setUp()

    def test_index_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_content_index_view(self):
        self.assertContains(self.response, 'Личный кабинет')


# class TestAuthViews(TestCase):
#     def setUp(self):
#         self.my_user = User.objects.create(
#             username='Ivan',
#             password='test',
#             email='ivan@test.com')
#         self.my_user.save()
#         super().setUp()

#     def test_login_redirect(self):
#         self.client.login(username='Ivan',
#                           password='test')
#         request = self.client.post('login/',)
#         self.assertRedirects(request, '',)
