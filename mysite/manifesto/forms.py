from django import forms
from datetime import datetime

from .models import Enrolment, Person, Session

class EnrolmentForm(forms.Form):

    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)
    email = forms.EmailField()
    parent_email = forms.EmailField()
    phone = forms.CharField(max_length=255, required=False)
    highschool = forms.CharField(max_length=255, required=False)

    level_programing = forms.IntegerField()
    level_python = forms.IntegerField()
    
    session = forms.ModelMultipleChoiceField(queryset=Session.objects.all(),
                                    widget=forms.CheckboxSelectMultiple(choices=Session.objects.all()),
                                    required=True
                                    )

    confirmation_email = forms.BooleanField()

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

    # botcheck = forms.CharField(max_length=6)


    def clean(self):
        data = super(EnrolmentForm, self).clean()
        email = data.get('email')
        parent_email = data.get('parent_email')

        if email == parent_email:
            self._errors['parent_email'] = self.error_class(['Les deux addresses mails doivent être différentes.'])
            del self.cleaned_data['parent_email']

        return data





