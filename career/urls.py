from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from career import views
from career.views import candidates, candidate_detail

urlpatterns=[
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('jobseeker_dashboard', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('hr_dashboard', views.hr_dashboard, name='hr_dashboard'),
    path('career/', views.career, name='career'),
    path('apply/', views.apply, name='apply'),#for apply actions
    # path('hr/dashboard/', hr_dashboard, name='hr_dashboard'),
    path('candidates/', candidates, name='candidates'),
    path('hr/candidates/<int:candidate_id>/', candidate_detail, name='candidate_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
