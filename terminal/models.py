from django.db import models
from django.utils import timezone
from datetime import datetime

class Tura(models.Model):
    nr=models.IntegerField()
    data=models.DateField()

    def __str__(self):
        return_string=str(self.nr) + "(" + str(self.data) + ")"
        return str(return_string)

class TA(models.Model):
    tura=models.ForeignKey(Tura)
    nr=models.IntegerField()
    elementy=models.TextField()
    zakonczone=models.BooleanField(default=False)

    def __str__(self):
        return str(self.nr, sefl.zakonczone)

# Create your models here.
class Etykieta(models.Model):
    ta=models.ForeignKey(TA)
    nr=models.IntegerField()
    pozycja=models.IntegerField(null=True)
    element=models.TextField(null=True)

    def __str__(self):
        return str(self.nr)

# Tabela odkladcza na Szwalni
class Wozek(models.Model):
    wozek=models.IntegerField()
    data_dodania=models.DateTimeField(default=timezone.now)
    data_wydania=models.DateTimeField(null=True)
    ta=models.ForeignKey(TA)
    odebrany=models.BooleanField(default=False)    

    def __str__(self):
        return str(self.wozek)

#Tabela odkladcza na Stolarni
class Pole(models.Model):
    pole=models.IntegerField()
    data_dodania=models.DateTimeField(default=timezone.now)
    data_wydania=models.DateTimeField(null=True)
    ta=models.ForeignKey(TA)

    def __str__(self):
        return str(self.pole)

class Szwalnia_status(models.Model):
    ta=models.ForeignKey(TA)
    zakonczone=models.BooleanField(default=False)
    ilosc=models.IntegerField(default=1)

    def __str__(self):
        return str(self.ta.nr)

class Stolarnia_status(models.Model):
    ta=models.ForeignKey(TA)
    zakonczone=models.BooleanField(default=False)
    ilosc=models.IntegerField(default=1)

    def __str__(self):
        return str(self.ta.nr)

class Bufor_status(models.Model):
    ta=models.ForeignKey(TA)
    zakonczone=models.BooleanField(default=False)
    ilosc=models.IntegerField(default=1)

    def __str__(self):
        return str(self.ta.nr)        


class Kolejnosc(models.Model):
    tura=models.TextField()
    data=models.DateField()

    def __str__(self):
        return_string=str(self.tura) + "(" + str(self.data) + ")"
        return return_string