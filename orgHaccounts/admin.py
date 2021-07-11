from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FileUpload, ScreenAnswer, VaccineResponse
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'date_of_birth', 'staff', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
@admin.register(FileUpload)
class FileUpload(admin.ModelAdmin):
    list_display=("file", "user")
@admin.register(VaccineResponse)
class VaccineResponseAdmin(admin.ModelAdmin):
    list_display=("vaccine_type", "vaccine_dose", "vaccine_location", "vaccine_illness", "user")
@admin.register(ScreenAnswer)
class ScreenAnswerAdmin(admin.ModelAdmin):
    list_display=("answer", "user")