from django import forms
from datetime import datetime
from phonenumber_field.formfields import PhoneNumberField

from .models import Enrolment, Person, Session

class EnrolmentForm(forms.Form):

    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)
    email = forms.EmailField()
    parent_email = forms.EmailField()
    phone = PhoneNumberField(widget=forms.TextInput(), required=True)#forms.CharField(max_length=255)
    highschool = forms.CharField(max_length=255, required=False)

    level_programing = forms.IntegerField()
    level_python = forms.IntegerField()
   
    session_queryset = Session.objects.all().filter(open_bool=True)
    
    # not working yet:
    #session = forms.ChoiceField(queryset=session_queryset,
    #                            widget=forms.RadioSelect(Choices=Session.objects.all(),
    #                                required=True)
    session = forms.ModelMultipleChoiceField(queryset=session_queryset,                        
            widget=forms.CheckboxSelectMultiple(choices=Session.objects.all()),
                                    required=True)
    n_sessions = len(session_queryset)

    confirmation_email = forms.BooleanField(initial=False)

    def save(self):
        data = self.cleaned_data

        student = Person(firstname=data['firstname'],
                        lastname=data['lastname'],
                        email=data['email'],
                        parent_email=data['parent_email'],
                        phone=data['phone'],
                        highschool=data['highschool'])

        ##if student exists already don't save
        if not Person.objects.filter(firstname=data['firstname'], 
                                     lastname=data['lastname'], 
                                     email=data['email']).exists():
            student.save()
        else:
            student = Person.objects.filter(firstname=data['firstname'], 
                                            lastname=data['lastname'], 
                                            email=data['email'])[0]

        enrolment = Enrolment(student=student,
                            level_programing=data['level_programing'],
                            level_python=data['level_python'],
                            confirmation_email=data['confirmation_email'])
        enrolment.save()
        enrolment.session.set(data['session'])
        enrolment.save()

    # botcheck = forms.CharField(max_length=6)


    def clean(self):
        data = super(EnrolmentForm, self).clean()
        email = data.get('email')
        parent_email = data.get('parent_email')

        if email == parent_email and (email != None):
            self._errors['parent_email'] = self.error_class(['Les deux addresses mails doivent être différentes.'])
            print(email, parent_email)
            del self.cleaned_data['parent_email']

        return data

