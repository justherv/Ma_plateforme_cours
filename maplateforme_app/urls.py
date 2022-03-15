#import registration
#import registration
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('etudiant_list', views.etudiant_list, name='etudiant_list'),
    #path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('etudiant/new/', views.etudiant_new, name='etudiant_new'),
    path('etudiant_list/(?P<id>\d+)/$', views.etudiant_edit, name='etudiant_edit'),
    #path('question/edit/', views.question_edit, name='question_edit'),
    #path('question_list/delete/', views.question_delete, name='question_delete'),
    path('etudiant_list/(?P<id>\d+)/delete$', views.etudiant_delete, name='etudiant_delete'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #path('', views.home, name='home'),

#------------------------------Filières---------------------
    path('filiere_list', views.filiere_list, name='filiere_list'),
    path('filiere/new/', views.filiere_new, name='filiere_new'),
    path('filiere_list/(?P<id>\d+)/$', views.filiere_edit, name='filiere_edit'),
    path('filiere_list/<int:id>/delete', views.filiere_delete, name='filiere_delete'),

#------------------------------Cours---------------------
    path('cours_list', views.cours_list, name='cours_list'),
    path('cours/new/', views.cours_new, name='cours_new'),
    path('cours_list/(?P<id>\d+)/$', views.cours_edit, name='cours_edit'),
    path('cours_list/<int:id>/delete', views.cours_delete, name='cours_delete'),


#------------------------------TP---------------------
    path('tp_list', views.tp_list, name='tp_list'),
    path('tp/new/', views.tp_new, name='tp_new'),
    path('tp_list/(?P<id>\d+)/$', views.tp_edit, name='tp_edit'),
    path('tp_list/<int:id>/delete', views.tp_delete, name='tp_delete'),

#------------------------------Examen Cours--------------------
    path('examencours_list', views.examencours_list, name='examencours_list'),
    path('examencours/new/', views.examencours_new, name='examencours_new'),
    path('examencours_list/(?P<id>\d+)/$', views.examencours_edit, name='examencours_edit'),
    path('examencours_list/<int:id>/delete', views.examencours_delete, name='examencours_delete'),

#------------------------------Examen TP--------------------
    path('examentp_list', views.examentp_list, name='examentp_list'),
    path('examentp/new/', views.examentp_new, name='examentp_new'),
    path('examentp_list/(?P<id>\d+)/$', views.examentp_edit, name='examentp_edit'),
    path('examentp_list/<int:id>/delete', views.examentp_delete, name='examentp_delete'),


#------------------------------Support de Cours--------------------
    path('supportcours_list', views.supportcours_list, name='supportcours_list'),
    path('supportcours/new/', views.supportcours_new, name='supportcours_new'),
    path('supportcours_list/(?P<id>\d+)/$', views.supportcours_edit, name='supportcours_edit'),
    path('supportcours_list/<int:id>/delete', views.supportcours_delete, name='supportcours_delete'),


#------------------------------Support de TPs--------------------
    path('supportp_list', views.supportp_list, name='supportp_list'),
    path('supportp/new/', views.supportp_new, name='supportp_new'),
    path('supportp_list/(?P<id>\d+)/$', views.supportp_edit, name='supportp_edit'),
    path('supportp_list/<int:id>/delete', views.supportp_delete, name='supportp_delete'),


]

#------------------------------upload files-------------------
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






