import codecs
import os
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from datetime import datetime, timedelta
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Post, Profile


class TestPostModel(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = os.path.join(dir_, 'static', 'test.jpg')
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        f.close()

        self.my_user = User.objects.create(
            username='Ivan',
            password='test',
            email='ivan@test.com')

        self. my_post = Post.objects.create(
            author=self.my_user,
            post_name='name',
            description='description',
            price='35',
        )
        self.my_user.save()
        self.my_post.save()
        super().setUp()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_date_edit(self):
        with self.assertRaises(ValidationError):
            self.my_post.date_edit = datetime.now() + timedelta(days=1)
            self.my_post.full_clean()
            self.my_post.save()


class TestProfileModel(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = os.path.join(dir_, 'static', 'test.jpg')
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        f.close()

        self.my_user = User.objects.create(
            username='Ivan',
            password='test',
            email='ivan@test.com')
        self.my_user.save()
        super().setUp()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_profile_with_user(self):
        self.assertIsNotNone(self.my_user.profile, 'Профиль не создан!!!')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_birth_date_with_future_date(self):
        with self.assertRaises(ValidationError):
            self.my_user.profile.birth_date = datetime.datetime.now() + \
                datetime.timedelta(days=1)
            self.my_user.profile.save()
            self.my_user.profile.full_clean()
