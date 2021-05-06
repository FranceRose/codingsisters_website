from .models import Enrolment, Session, Person
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import EnrolmentForm
from django.utils import timezone
from django.template import RequestContext

def enrolment_new(request):

    sender_email = 'contact@codingsisters.fr'

    if request.method == "POST":
        form = EnrolmentForm(request.POST)

        if form.is_valid():

            form.save()

            email = form.cleaned_data['email']
            parent_email = form.cleaned_data['parent_email']
            confirmation_email = form.cleaned_data['confirmation_email']

            email_body_raw, email_body_pretty = format_email(form, request)
            send_mail("[admin-CS] Inscription", email_body_raw, sender_email, [sender_email])

            if confirmation_email:
                send_mail("Inscription aux Coding Sisters!", email_body_pretty, sender_email, [email, parent_email])

            return redirect('enrolment_thankyou', confirmation_email, email)

        else:
            print('form not valid')
            return render(request, 'manifesto/enrolment_new.html', {'form':form})

    else:
        form = EnrolmentForm()
        return render(request, 'manifesto/enrolment_new.html', {'form': form})


def format_email(form, request):
    email_body_raw = ""
    data = {}
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

        email_body_raw += "{}: {}\n".format(f, datum)
        data[f]= datum
     
    email_body_pretty = "Bonjour {prenom},\n\nmerci de ton inscription aux Coding Sisters pour la session d{session}- de 17h à 19h (CET) !\n\nQuelques vérifications avant de valider ton inscription :\n- as-tu bien pris connaissance que ce tutorat était à destination des filles et minorités de genre ?\n- actuellement, avec la pandémie de Covid, les tutorats se font en ligne. Auras-tu accès à un ordinateur, une connexion internet et si possible un micro ?\n- les tutorats sont en français. Il faut un bon niveau de langue pour suivre. En effet, il est difficile de bien comprendre Python et les concepts de programmation si, et la langue, et le distanciel se mettent en travers.\n\nCoding Sisters est une initiative qui fonctionne grâce à nos encadrantes bénévoles. Par cette inscription, tu t’engages à participer à toutes les seances. S’il te plaît, ne nous fais pas perdre notre temps et ne prends pas la place de quelqu’une en liste d’attente si tu n’es pas sûre de vouloir et/ou pouvoir suivre toutes les séances !\n\nPour valider ton inscription, lis bien la charte (https://www.codingsisters.fr/static/images/Charte_CodingSisters_2021.pdf) et renvoie-la nous signée. Attention, sans la charte, ton inscription ne sera pas prise en compte.\n\nSi tout est bon, nous te contacterons une à deux semaines avant la première séance pour les détails.\n\nÀ très vite on espère,\nLes Coding Sisters.".format(prenom=data['firstname'], session=data['session'][1:-2])    
    return email_body_raw, email_body_pretty

"""
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


"""
def enrolment_thankyou(request, confirmation_email, email):
    return render(request, 'manifesto/enrolment_thankyou.html', 
                     {'confirmation_email': confirmation_email, 'email': email}
                  )


def manifesto(request):
    return render(request, 'manifesto/manifesto.html')
