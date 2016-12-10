from django.shortcuts import render, get_object_or_404
from terminal.models import Etykieta, Szwalnia_status, Stolarnia_status, Bufor_status, Kolejnosc, Tura
from django.db.models import Count
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def szwalnia_przekaz(request):
    try:
        nr_wozka=int(request.POST['wozek'])
        nr_etykiety=int(request.POST['etykieta'])
        Etyk=Etykieta.objects.get(nr=nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/szwalnia/przekaz.html', {'error': True,
                                                        'message': 'Niepoprawne dane!'})

    T=Etyk.ta
    s=Szwalnia_status.objects.get(ta=T)
    if T.zakonczone == True:
        return render(request, 'terminal/szwalnia/przekaz.html', {'error': True,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        w=Wozek(ta=T, wozek=nr_wozka)
        s.szwalnia_ilosc -= 1
        if s.szwalnia_ilosc == 0:
            T.zakonczone=True
        w.save()
        s.save()
        T.save()
        message_string='Dodano TA %s na wózek %s' % (T.nr, nr_wozka)
        context_dict={
        'success': True,
        'message': message_string,
        }
        return render(request, 'terminal/szwalnia/przekaz.html', context_dict)


def szwalnia(request):
    if not request.POST:
        return render(request, 'terminal/szwalnia/status.html', {})
    try:
        nowa_data=datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/szwalnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc=Kolejnosc.objects.filter(data=nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci=[]
    lista_dat=[]
    ordered_list=()
    for each in kolejnosc:
        tury=Tura.objects.filter(nr=each.tura, data=each.data).first()
        ilosci_pozostale=tury.ta_set.all().filter(zakonczone=True).count()
        try:
            procent=int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent=0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict={
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/szwalnia/status.html', context_dict)

# ---------------------------------------------------------------------------
#STOLARNIA
@csrf_exempt
def stolarnia_przekaz(request):
    try:
        nr_pola=int(request.POST['pole'])
        nr_etykiety=int(request.POST['etykieta'])
        Etyk=Etykieta.objects.get(nr=nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/stolarnia/przekaz.html', {'error': True,
                                                        'message': 'Niepoprawne dane!'})

    T=Etyk.ta
    s=Stolarnia_status.objects.get(ta=T)
    if T.zakonczone == True:
        return render(request, 'terminal/stolarnia/przekaz.html', {'error': True,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        w=Pole(ta=T, pole=nr_pola)
        s.stolarnia_ilosc -= 1
        if s.stolarnia_ilosc == 0:
            T.zakonczone=True
        w.save()
        s.save()
        T.save()
        message_string='Dodano TA %s na pole %s' % (T.nr, nr_wozka)
        context_dict={
        'success': True,
        'message': message_string,
        }
        return render(request, 'terminal/stolarnia/przekaz.html', context_dict)


def stolarnia(request):
    if not request.POST:
        return render(request, 'terminal/stolarnia/status.html', {})
    try:
        nowa_data=datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/stolarnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc=Kolejnosc.objects.filter(data=nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci=[]
    lista_dat=[]
    ordered_list=()
    for each in kolejnosc:
        tury=Tura.objects.get(nr=each.tura, data=each.data)
        ilosci_pozostale=tury.ta_set.all().filter(zakonczone=True).count()
        try:
            procent=int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent=0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict={
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/stolarnia/status.html', context_dict)

# ---------------------------------------------------------------------------
#BUFOR
def bufor_przekaz(request):
    render(request, 'terminal/bufor/przekaz', context_dict)

def bufor_oddaj(request):
    wozek=int(request.POST['wozek'])
    status_wozka=Wozek.objects.filter(wozek=wozek, odebrany=True)
    if len(status_wozka) == 0:
        render(request, 'terminal/bufor/oddaj', context_dict={'error': 'Blad krytyczny! Wezwij administratora sieci!'})
    for each in status_wozka:
        each.delete()
    message="Wozek %i oddany na szwalnie" % wozek
    context_dict={
    'message': message,
    }
    render(request, 'terminal/bufor/oddaj', context_dict)

def bufor_potwierdz(request):
    wozek=int(request.POST['wozek'])
    status_wozka=Wozek.objects.filter(wozek=wozek, odebrany=False)
    if len(status_wozka) == 0:
        render(request, 'terminal/bufor/potwierdz', context_dict={'error': 'Podany wozek nie posiada seskanowanych kompletow!'})
    for each in status_wozka:
        s=each.ta.bufor_status_set.first()
        each.odebrany=True
        each.save()
    context_dict={
    'message': status_wozka,
    }
    render(request, 'terminal/bufor/potwierdz', context_dict)

def bufor_sprawdz(request):
    render(request, 'terminal/bufor/sprawdz', context_dict)

def bufor(request):
    render(request, 'terminal/bufor/status', context_dict)

# ---------------------------------------------------------------------------
#TESTOWA
@csrf_exempt
def Testowa(request):
    try:
        nr_wozka=int(request.POST['wozek'])
        nr_etykiety=int(request.POST['etykieta'])
        Etyk=Etykieta.objects.get(nr=nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/testowa.html', {'error': True,
                                                        'message': 'Niepoprawne dane!'})
    T=Etyk.ta
    s=Status.objects.get(ta=T)
    if T.zakonczone == True:
        return render(request, 'terminal/testowa.html', {'error': True,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        w=Wozek(ta=T, wozek=nr_wozka)
        s.szwalnia_ilosc -= 1
        if s.szwalnia_ilosc == 0:
            T.zakonczone=True
        w.save()
        s.save()
        T.save()
        message_string='Dodano %s na wózek %s' % (T.nr, nr_wozka)
        context_dict={
        'success': True,
        'message': message_string,
        }
        return render(request, 'terminal/testowa.html', context_dict)
