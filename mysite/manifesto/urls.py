from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.manifesto, name='manifesto'),
    path('enrolment/new/', views.enrolment_new, name='enrolment_new'),
    path('enrolment/thankyou_<str:confirmation_email>_<str:email>', views.enrolment_thankyou, name='enrolment_thankyou'),
]