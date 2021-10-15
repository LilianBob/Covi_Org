from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import OrgHUser, FileUpload,ScreenAnswer, VaccineResponse, NewsPost, Comment, Like 

User = get_user_model()

class OrgHUserTestCase(TestCase):
    def create_user(self, email="licell@gmail.com", date_of_birth="2021-10-15", password="testT6789"):
        return User.objects.create(email=email, date_of_birth=date_of_birth, password="password")
    def test_create_user(self):
        myuser = self.create_user()
        self.assertTrue(isinstance(myuser, OrgHUser))
        self.assertEqual(myuser.__str__(), myuser.email)

class ScreenAnswerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email="licell@gmail.com", date_of_birth="2021-10-15", password="testT6789")
        ScreenAnswer.objects.create(
            answer='Yes',
            user= test_user
        )

    def test_answer_max_length(self):
        answer = ScreenAnswer.objects.get(id=1)
        max_length = answer._meta.get_field('answer').max_length
        self.assertEqual(max_length, 25)

# class VaccineResponseTestCase(TestCase):
# class FileUploadTestCase(TestCase):
# class NewsPostTestCase(TestCase):
# class CommentTestCase(TestCase):   
# class LikeTestCase(TestCase):
