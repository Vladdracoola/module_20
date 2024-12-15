"""
URL configuration for Finish_line project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Detection_platform.views import main, sign_up, log_in, log_out, detection, delete_image, add_image, process_image_feed
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('registration/', sign_up, name='registration'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('detection/', detection, name='detection'),
    path('process/<int:feed_id>/', process_image_feed, name='process_feed'),
    path('image/delete/<int:image_id>/', delete_image, name='delete_image'),
    path('add_image/', add_image, name='add_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
