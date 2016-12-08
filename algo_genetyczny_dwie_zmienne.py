from __future__ import division
from random import uniform, randint

punkt_podzialu_x1 = randint(1, 11)
punkt_podzialu_x2 = randint(13, 23)
punkt_podzialu_na_x1_x2 = 12
populacja = 10
ilosc_bitow = 24
wartosci_funkcji = []

tablica_chromosomow = tablica_par = tablica_chromosomow_potomkow = [["" for x in range(ilosc_bitow)] for y in range(populacja)]


def random():
    return uniform(0, 1)


def chromosom2decimal(chromosom, poczatek):
    wynik = 0
    i = poczatek
    for x in chromosom:
        if x == 1:
            wynik += 2**i
        i += 1
    return wynik


def wartosc_x_do_funkcji(x):
    return -2.048 + (x * 4.096) / (2**24 - 1)  # NA PEWNO TAKA DOKLADNOSC??


def losowanie():
    for nr in xrange(0, populacja):
        for i in xrange(0, ilosc_bitow):
            if random() > 0.5:
                tablica_chromosomow[nr][i] = 1
            else:
                tablica_chromosomow[nr][i] = 0
    return tablica_chromosomow


def oblicz_funkcje_celu(chromosom):
    x1 = wartosc_x_do_funkcji(chromosom2decimal(chromosom[0:punkt_podzialu_na_x1_x2], 0))
    x2 = wartosc_x_do_funkcji(chromosom2decimal(chromosom[punkt_podzialu_na_x1_x2:ilosc_bitow], 12))
    f = 100*(x1**2 - x2)**2 + (1 - x1)**2
    return f


def ruletka():
    rand = uniform(0, 1)
    for i in xrange(0, populacja):
        if rand < tablica_skumulowane_p[i]:
            osobnik = tablica_chromosomow[i]
            break
    return osobnik


losowanie()

# ITERACJE ALGORYTMU
for i in xrange(0, 10000):
    suma = 0
    y = []
    prawdopodobienstwa = []
    tablica_skumulowane_p = []
    skumulowane_p = 0

    # OBLICZANIE SUMY WARTOSCI FUNKCJI CELU
    for i in xrange(0, populacja):
        y.append(oblicz_funkcje_celu(tablica_chromosomow[i]))
        suma += y[i]

    # OBLICZANIE PRAWDOPODOBIENSTW
    for i in xrange(0, populacja):
        prawdopodobienstwa.append((y[i]/suma))

    # OBLICZANIE SKUMULOWANYCH PRAWDOPODOBIENSTW
    for i in xrange(0, populacja):
        skumulowane_p += prawdopodobienstwa[i]
        tablica_skumulowane_p.append(skumulowane_p)

    # WYBIERANIE PAR OSOBNIKOW
    nr = 0
    while nr < populacja:
        osobnik1 = ruletka()
        osobnik2 = ruletka()
        if osobnik1 != osobnik2:
            tablica_par[nr] = osobnik1
            tablica_par[nr+1] = osobnik2
            nr += 2

    # KRZYZOWANIE
    if random() < 0.8:
        nr = 0
        while nr < populacja:
            for i in xrange(0, ilosc_bitow):
                if i < punkt_podzialu_na_x1_x2:
                    if i < punkt_podzialu_x1:
                        tablica_chromosomow_potomkow[nr][i] = tablica_par[nr][i]
                        tablica_chromosomow_potomkow[nr+1][i] = tablica_par[nr+1][i]
                    else:
                        tablica_chromosomow_potomkow[nr][i] = tablica_par[nr+1][i]
                        tablica_chromosomow_potomkow[nr+1][i] = tablica_par[nr][i]
                else:
                    if i < punkt_podzialu_x2:
                        tablica_chromosomow_potomkow[nr][i] = tablica_par[nr][i]
                        tablica_chromosomow_potomkow[nr+1][i] = tablica_par[nr+1][i]
                    else:
                        tablica_chromosomow_potomkow[nr][i] = tablica_par[nr+1][i]
                        tablica_chromosomow_potomkow[nr+1][i] = tablica_par[nr][i]
            nr += 2
    else:
        tablica_chromosomow_potomkow = tablica_par

    # MUTOWANIE
    nr = 0
    while nr < populacja:
        for i in xrange(0, ilosc_bitow):
            if tablica_chromosomow_potomkow[nr][i] == 0:
                if random() < 0.05:
                    tablica_chromosomow_potomkow[nr][i] = 1
            else:
                if random() < 0.05:
                    tablica_chromosomow_potomkow[nr][i] = 0
        nr += 1

    tablica_chromosomow = tablica_chromosomow_potomkow

    for i in xrange(0, populacja):
        wartosci_funkcji.append(oblicz_funkcje_celu(tablica_chromosomow[i]))
    print min(wartosci_funkcji)
    print ""


print "Znaleziona minimalna wartosc funkcji wynosi: %f" % min(wartosci_funkcji)