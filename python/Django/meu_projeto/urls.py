from django.urls import path, include
from django.contrib import admin
from meu_projeto import views as meu_projeto_views
from Dashboard import views as dashboard_views
from django.contrib.auth import views as auth_views
from socket import socket
from meu_projeto.forms import LoginForm
from django.conf.urls import url
from django.urls import re_path
from django.urls import path, include
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', meu_projeto_views.TelaInicial, name='TelaInicial'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('login/', meu_projeto_views.CustomLoginView.as_view(redirect_authenticated_user=False, template_name='users/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', meu_projeto_views.logout_view, name='logout'),
    path('CriarConta/', meu_projeto_views.home, name='CriarConta'),
    path('SaibaMais/', meu_projeto_views.SaibaMais, name='SaibaMais'),
    path('Dashboard', dashboard_views.dashboard, name='dashboard'),
    path('enviar_mensagem', dashboard_views.enviar_mensagem, name='enviar_mensagem'),
    path('register/', meu_projeto_views.RegisterView.as_view(), name='RegisterView'),
    path('', include('Dashboard.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('password-reset/', meu_projeto_views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
