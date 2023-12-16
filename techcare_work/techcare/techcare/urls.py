"""
URL configuration for techcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from techcare.userapp.views import SignUpView
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name = "index.html"), name = "home"),
    path('about/', TemplateView.as_view(template_name = "about.html"), name = "about"),
    path('doctors/', TemplateView.as_view(template_name = "doctors.html"), name = "doctors"),
    path('contact/', TemplateView.as_view(template_name = "contact.html"), name = "contact"),
    path('blog/', TemplateView.as_view(template_name = "blog.html"), name = "blog"),
    path('blog_details', TemplateView.as_view(template_name = "blog-details.html"), name = "blog_details"),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name= "signup"),
    re_path(r'^userapp/', include("techcare.userapp.urls")),
    re_path(r'consultapp/', include('techcare.consultapp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
