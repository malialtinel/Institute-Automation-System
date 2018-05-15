"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from Campus.views import *
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('student_courses/<pk>/', student_courses, name="student_courses"),
    path('login/', views.login, {'template_name': 'login.html'},name='login'),
    path('logout/', views.logout, name='logout'),   path('', home, name='home'),
    path('special_quota', special_quota, name='special_quota'),
    path('open_special_quota', open_special_quota, name='open_special_quota'),
    path('harf_notu/', harf_notu, name='harf_notu'),
    path('get_section_students/<pk>/', get_section_students, name="get_section_students"),
    path('give_note/', give_note, name="give_note"),
    path('studentsOfAdvisor/<pk>/', display_students,name="dana"),
    path('changeQuota/<pk>/', SectionUpdateView.as_view()),


    path('studentsOfMyCourses/', studentsOfMyCourses,name="studentsOfMyCourses"),
    path('myStudents/', myStudents,name="myStudents"),
    path('base/', base),
    path('displayTranscript/<st_id>/', displayTranscript),
    path('displaySchedule/<st_id>/', displaySchedule),
    path('displayCCR/<st_id>/', displayCCR),
    path('displayCurriculum/<st_id>/', displayCurriculum),
    path('myCourses/', myCourses , name="myCourses"),
    path('myCourseDetails/<pk>/', myCourseDetails),
    path('grade/<st_id>/', grade),
    path('openNewSection/', openNewSection),
    path('Reject/<st_id>/', ScheduleApproveOrReject,name="ScheduleApproveOrReject"),
    path('sectionlar/', sectionlar,name="sectionlar"),

]
