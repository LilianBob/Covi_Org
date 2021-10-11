from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings

User = settings.AUTH_USER_MODEL

class OrgHUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class OrgHUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(
        verbose_name='birth date',
    )
    avatar= models.ImageField(
        upload_to='profile_images', 
        default= 'profile_images/default.jpg',
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    last_login= models.DateTimeField(auto_now=True, null=True)

    objects = OrgHUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff
    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

# class UserAvatar(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar= models.ImageField(upload_to='profile_images', default='default.jpg')

class ScreenAnswer(models.Model):
    answer= models.CharField(max_length=25)
    user= models.ForeignKey(User, related_name="screenAnswers", on_delete=models.SET_NULL, null=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    updated_at= models.DateTimeField(auto_now=True, null=True)

class VaccineResponse(models.Model):
    vaccine_type= models.CharField(max_length=25) 
    vaccine_dose= models.CharField(max_length=25) 
    date_received = models.DateField(verbose_name='Vaccination date',)
    vaccine_location= models.CharField(max_length=25)
    vaccine_illness= models.TextField(max_length=1000)
    user= models.ForeignKey(User, related_name="vaccineResponses", on_delete=models.SET_NULL, null=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    updated_at= models.DateTimeField(auto_now=True, null=True)

class FileUpload(models.Model):
    file= models.FileField(upload_to="user_docs", null=True, blank=True)
    user= models.ForeignKey(User, related_name="fileUploads", on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now=True)
    updated_at= models.DateTimeField(auto_now_add=True)

class NewsPostManager(models.Manager):
    def validate_newsPost(self, newsPost_description):
        errors = {}
        if len(newsPost_description) < 10:
            errors['length'] = 'Posts must be at least 10 characters'
        if len(newsPost_description) > 100:
            errors['length'] = f"Posts must be less than 101 characters. Current is {len(newsPost_description)}"
        return errors

class NewsPost(models.Model):
    intro = models.CharField(max_length=255)
    newscover = models.ImageField(upload_to='news_images/', default='news_images/get_social.jpg')
    title = models.CharField(max_length=255)
    description= models.TextField()
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='liked_newsposts')
    postContent= models.TextField()
    creator = models.ForeignKey(User, related_name='newsPosts', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="users", null=True)
    newsPost = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="posts")
    alreadyLiked = models.BooleanField(default=False)

class Comment(models.Model):
    newsPost_comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.SET_NULL, null=True)
    newsPost = models.ForeignKey(NewsPost, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)