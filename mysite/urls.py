"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("""
    <h1>🚀 Laravel風 AI Development Platform</h1>
    <p>Django + FastAPI + Gradio 統合システム</p>
    <ul>
        <li><a href="/admin/">🔧 Django Admin</a></li>
        <li><a href="/gradio/">💬 Gradio Chat</a></li>
        <li><a href="/docs/">📋 API Documentation</a></li>
    </ul>
    """)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),  # ホームページ
]
