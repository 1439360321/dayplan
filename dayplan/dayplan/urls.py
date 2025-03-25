"""
URL configuration for dayplan project.

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
# schedule_project/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, LoginView, ProfileView, ChangePasswordView, get_csrf_token,logout_view
from tasks.views import TaskListCreateView, TaskDetailView, ExportTasksPDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    # 任务管理路由后面会补充
    path('api/tasks/', TaskListCreateView.as_view(), name='tasks'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/export-pdf/', ExportTasksPDFView.as_view(), name='export-pdf'),
    # django-allauth 第三方登录
    path('accounts/', include('allauth.urls')),
    path("api/csrf/", get_csrf_token),  # 让前端 Vue 访问 http://localhost:9000/api/csrf/ 获取 CSRF 令牌
    path('logout/', logout_view, name='logout')
]

