from django.urls import path, include
# from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'results'


urlpatterns = [
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(template_name='logged_out.html'), name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
