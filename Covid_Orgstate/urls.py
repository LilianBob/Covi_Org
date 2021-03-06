"""Covid_Orgstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from orgHaccounts.admin import admin_site
from django.urls import path, include, reverse_lazy, get_resolver
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
get_resolver(None)

urlpatterns = [
    path('', include('orgHaccounts.urls')),
    path('oHadmin/', admin_site.urls),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(success_url=reverse_lazy('password_reset_done')),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path('password_change/',
        auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')), 
        name='password_change'
        ),
    path('password_change/done/', 
        auth_views.PasswordChangeDoneView.as_view(), 
        name='password_change_done'
        ),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)