"""
URL configuration for web_db_project project.

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
from web_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(next_page='home'), name='logout'),

    path('userdetail/<int:pk>/', views.CustomUserDetailView.as_view(), name='user_detail'),
    path('userupdate/<int:pk>/', views.CustomUserUpdateView.as_view(), name='user_update'),
    path('passwordchange/<int:pk>', views.CustomPasswordChangeView.as_view(), name='password_change'),

    path('', views.home, name='home'),
    path('trainingplans', views.TrainingPlansListView.as_view(), name='training_plans'),
    path('trainingplandetail/<int:pk>/', views.training_plan_detail, name='training_plan_detail'),
]
