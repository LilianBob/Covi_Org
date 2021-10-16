from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
# from django_markdown.admin import MarkdownModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FileUpload, ScreenAnswer, VaccineResponse,NewsPost, Comment, Like
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()
class OHAdminSite(AdminSite):
    site_header = 'Orghealth administration'

admin_site = OHAdminSite(name='oHadmin')

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'date_of_birth', 'avatar', 'staff', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'avatar')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'avatar', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin_site.register(User, UserAdmin)
@admin.register(FileUpload, site=admin_site)
class FileUpload(admin.ModelAdmin):
    list_display=("file", "user")
@admin.register(VaccineResponse, site=admin_site)
class VaccineResponseAdmin(admin.ModelAdmin):
    list_display=("vaccine_type", "vaccine_dose", "date_received", "vaccine_location", "vaccine_illness", "user")
@admin.register(ScreenAnswer, site=admin_site)
class ScreenAnswerAdmin(admin.ModelAdmin):
    list_display=("answer", "user")
@admin.register(NewsPost, site=admin_site)
class NewsPostAdmin(admin.ModelAdmin):
    list_display=("intro", "title", "newscover", "description", "postContent", "creator")
@admin.register(Like, site=admin_site)
class LikeAdmin(admin.ModelAdmin):
    list_display=("newsPost", "alreadyLiked", "user")
@admin.register(Comment, site=admin_site)
class CommentAdmin(admin.ModelAdmin):
    list_display=("newsPost_comment", "newsPost", "user")