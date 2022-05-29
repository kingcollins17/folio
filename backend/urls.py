from django.urls import path
from . import views
from knox import views as knox_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('port/', views.ProfileView.as_view()),
    path('auth/register/', views.RegisterAPI.as_view()),
    path('auth/login/', views.LoginAPI.as_view()),
    path('auth/user/', views.UserAPI.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view()),
    path('port/manage/', views.ProfileManageAPI.as_view()),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
