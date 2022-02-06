from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime
import locale
from phonenumber_field.modelfields import PhoneNumberField


locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

class Session(models.Model):
    starting_date = models.DateField(default=datetime.now, blank=True)
    ending_date = models.DateField(default=datetime.now, blank=True)
    title = models.CharField(max_length=6, default='000000')
    open_bool = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.title = self.starting_date.strftime('%Y%m')
        super().save(*args, **kwargs)
    
    def __str__(self):
        duration = int((self.ending_date - self.starting_date).days / 7) + 1
        day_of_the_week = self.starting_date.weekday()
        day_of_the_week = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'][int(day_of_the_week)]
        return "Du {} {} {} au {} {} {} inclus - {} séances".format(day_of_the_week, 
                                                                    self.starting_date.strftime('%d'),
                                                                    self.starting_date.strftime('%B'),
                                                                    day_of_the_week,
                                                                    self.ending_date.strftime('%d'),
                                                                            self.ending_date.strftime('%B'),
                                                                            duration)



class Person(models.Model):

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField()
    parent_email = models.EmailField(null=True)
    phone = PhoneNumberField()#models.CharField(max_length=255, null=True)#PheNumberField()
    highschool = models.CharField(max_length=255)

    # botcheck = models.CharField(max_length=6)

    def __str__(self):
        return ' '.join([str(self.firstname), str(self.lastname)])

    class Meta:
        unique_together = ('firstname', 'lastname', 'email',)


class Enrolment(models.Model):

    student = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    level_programing = models.IntegerField(default=0)
    level_python = models.IntegerField(default=0)
    
    session = models.ManyToManyField(Session)

    confirmation_email = models.BooleanField(default=True)

    # botcheck = models.CharField(max_length=6)


