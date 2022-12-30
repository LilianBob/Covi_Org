from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import OrgHUser, ScreenAnswer, VaccineResponse, NewsPost 

User = get_user_model()

class OrgHUserTestCase(TestCase):
    def create_user(self, email="licell@gmail.com", password="testT6789"):
        return User.objects.create(email=email, password="password")
    def test_create_user(self):
        myuser = self.create_user()
        self.assertTrue(isinstance(myuser, OrgHUser))
        self.assertEqual(myuser.__str__(), myuser.email)

class ScreenAnswerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email="licell@gmail.com", password="testT6789")
        ScreenAnswer.objects.create(
            answer='Yes',
            user= test_user
        )

    def test_answer_max_length(self):
        answer = ScreenAnswer.objects.get(id=1)
        max_length = answer._meta.get_field('answer').max_length
        self.assertEqual(max_length, 3)

class VaccineResponseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email="licell@gmail.com", password="testT6789")
        VaccineResponse.objects.create(
            vaccine_type='pfizer_biontech',
            vaccine_dose='1',
            vaccine_illness='fever, headache, pain at injection site, and fatigue',
            date_received='2021-10-14',
            vaccine_location='Albertson, Washington Ave S',
            user= test_user
        )

    def test_vaccine_type(self ):
        vaccineResponse = VaccineResponse.objects.get(id=1)
        vaccine_type=vaccineResponse.vaccine_type
        self.assertEqual(vaccine_type, 'pfizer_biontech')
    def test_vaccine_dose_max_length(self ):
        vaccine_dose = VaccineResponse.objects.get(id=1)
        max_length = vaccine_dose._meta.get_field('vaccine_dose').max_length
        self.assertEqual(max_length, 8)

class NewsPostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email="licell@gmail.com", password="testT6789")
        test_user.staff = True
        test_user.save()
        NewsPost.objects.create(
            title='my friends are here',
            intro="We have been a part, now we are together",
            description="when you miss someone so much you want to munch them when you see them; resist",
            creator= test_user,
            likes= "1",
            postContent="Been waiting for the longest time"
        )
    def validate_newsPost(self, newsPost_description):
        errors = {}
        if len(newsPost_description) < 10:
            errors['length'] = 'Posts must be at least 10 characters'
        if len(newsPost_description) > 100:
            errors['length'] = f"Posts must be less than 101 characters. Current is {len(newsPost_description)}"
        return errors
    def test_creator(self ):
        newsPost = NewsPost.objects.get(id=1)
        creator=newsPost.creator
        self.assertEqual(creator.email, "licell@gmail.com")
    def test_description(self ):
        newsPost = NewsPost.objects.get(id=1)
        description=newsPost.description
        valid_description=self.validate_newsPost(newsPost_description=description)
        self.assertEqual(valid_description, {})
        self.assertTrue(isinstance(newsPost, NewsPost))
        self.assertEqual(newsPost.description,"when you miss someone so much you want to munch them when you see them; resist")