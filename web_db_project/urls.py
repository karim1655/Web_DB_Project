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
from django.conf import settings
from django.conf.urls.static import static

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
    path('courses', views.CoursesListView.as_view(), name='courses'),

    path('coursedetail/<int:pk>/', views.course_detail, name='course_detail'),
    path('coursecreate', views.CourseCreateView.as_view(), name='course_create'),
    path('courseupdate/<int:pk>/', views.CourseUpdateView.as_view(), name='course_update'),
    path('coursedelete/<int:pk>/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('courseupdate/<int:pk>/plannedupdate', views.planned_completed_update, name='planned_update'),
    path('courseupdate/<int:pk>/completedupdate', views.planned_completed_update, name='completed_update'),

    path('search', views.search, name='search'),

    path('coursedetail/<int:pk>/uploadfile', views.upload_file, name='upload_file'),
    path('coursedetail/<int:pk>/deletefile/<int:file_id>/', views.delete_file, name='delete_file'),

    path('coursedetail/<int:course_id>/addplannedattendance', views.add_planned_or_completed_attendance, name='add_planned_attendance'),
    path('coursedetail/<int:course_id>/addcompletedattendance', views.add_planned_or_completed_attendance, name='add_completed_attendance'),
    path('coursedetail/<int:course_id>/removeplannedattendance/<int:attendance_id>/', views.remove_planned_or_completed_attendance, name='remove_planned_attendance'),
    path('coursedetail/<int:course_id>/removecompletedattendance/<int:attendance_id>/', views.remove_planned_or_completed_attendance, name='remove_completed_attendance'),

    path('dashboard/', views.dashboard, name='dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
