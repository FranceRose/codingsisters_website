from .models import Enrolment, Session, Person
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import EnrolmentForm
from django.utils import timezone
from django.template import RequestContext


def enrolment_new(request):

    sender_email = 'france.rose@ens.fr'

    if request.method == "POST":
        form = EnrolmentForm(request.POST)

        if form.is_valid():

            form.save()

            email = form.cleaned_data['email']
            parent_email = form.cleaned_data['parent_email']
            confirmation_email = form.cleaned_data['confirmation_email']

            email_body = format_email(form, request)
            send_mail("[admin-CS] Inscription", email_body, sender_email, [sender_email])

            if confirmation_email:
                send_mail("Inscription aux Coding Sisters!", email_body, sender_email, [email, parent_email])

            return redirect('enrolment_thankyou', confirmation_email, email)

        else:
            print('form not valid')
            return render(request, 'manifesto/enrolment_new.html', {'form':form})

    else:
        form = EnrolmentForm()
        return render(request, 'manifesto/enrolment_new.html', {'form': form})


def format_email(form, request):
    email_body = ""

    for f in form.fields:

        if f == 'session':
            asked_sessions = request.POST.getlist(f)
            datum = ""
            for s in asked_sessions:
                datum += str(Session.objects.filter(pk=s)[0])
                datum +=' ; '

        elif f.startswith('level'):
            datum = form.cleaned_data[f]
            datum = "{} / 5".format(datum+1)

        else:
            datum = form.cleaned_data[f]

        email_body += "{}: {}\n".format(f, datum)

    return email_body



def enrolment_thankyou(request, confirmation_email, email):
    return render(request, 'manifesto/enrolment_thankyou.html', 
                     {'confirmation_email': confirmation_email, 'email': email}
                  )


def manifesto(request):
    return render(request, 'manifesto/manifesto.html')