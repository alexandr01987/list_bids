# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

api_router = DefaultRouter()
api_router.register(r'solvo_requests', views.SolvoRequestSet, basename='solvo_requests')
app_name = 'solvo_support'

urlpatterns = [
    path('api/', include(api_router.urls)),
    path('list-requests/<status_requests>/<type_requests>', views.list_requests, name='list-requests'),
    path('request-details/<type_request>/<solvo_number>', views.request_details, name='request-details'),
    path('change-request/<type_request>/<solvo_request_number>', views.change_request, name='change-request'),
    path('list-emails/<int:solvo_number_request>', views.list_emails, name='list-emails'),
    path('email-details/<int:id_email>', views.email_details, name='email-details'),
    path('list-bugs/<request_number>', views.list_bugs, name='list-bugs'),
    path('bug-details/<bug_number>', views.bug_details, name='bug-details'),
    path('call-procedures', views.call_procedures, name='call-procedures-list'),
    path('call-procedures/<name_of_procedure>', views.call_procedures, name='call-procedure'),
    path('search-in-email', views.find_requests_by_text, name='search-in-email'),
    path('', views.index, name='index'),
]
