# Pentru a semnala ca o stare este initiala, in fisierul de configurare va fi trecuta in stilul q0, s
# Acelasi lucru pentru starile finale, doar ca f in loc de s
# In actions, tranzitiile sunt de genul: stare_inceput, input, stare_viitoare


def citire_fisier(nume_fisier):
    # Adaug toate datele din fisier intr-o variabila

    fisier = []
    try:
        with open(nume_fisier) as f:
            for linie in f:
                fisier.append(linie)

        return fisier

    # Tratez cazul in care fisierul nu exista si trimit o eroare

    except:
        print("Fisierul nu exista")
        return None


def citire_secventa():
    with open("secventa.in") as f:
        return f.readline()


def file_parser(fisier):
    structura_fisier = {}  # Memorez structura fisierului intr un dictionar
    sectiune_curenta = ''

    for linie in fisier:
        if linie[0] == '[' and linie[-2] == ']':  # Verific daca linia curenta anunta inceputul unei noi sectiuni

            # Populez dictionarul in stilul structurii fisierului. Fiecare sectiune este o cheie ale carei valori sunt
            # datele care se afla in sectunea respectiva

            nume_sectiune = linie.rstrip('\n').strip(']').lstrip('[')
            sectiune_curenta = nume_sectiune
            if nume_sectiune not in structura_fisier:  # Sectiunea curenta este folosita ca o cheie
                if nume_sectiune == 'Actions':
                    structura_fisier[
                        nume_sectiune] = {}  # Daca sectiunea curenta este 'Actions' elementele care urmeaza sa fie citite vor si stocate tot intr un dictionar
                else:
                    structura_fisier[nume_sectiune] = []  # Daca sectiunea curenta nu este 'Actions' elementele care urmeaza sa fie citite vor fi stocate intr o lista
        else:
            if linie[0] != '#' and sectiune_curenta != '':  # Verific daca linia curenta este un comentariu, iar in caz afirmativ o ignor
                data = linie.rstrip('\n')

                if sectiune_curenta == 'Actions':
                    data = data.split(", ")  # Impart linia curenta in parti componente

                    if len(data) < 3:
                        print("Datele din Actions nu sunt complete")
                        return False

                    if data[0] not in structura_fisier[sectiune_curenta]:
                        structura_fisier[sectiune_curenta][data[0]] = {}  # Daca elementul nu a fost adaugat deja in actions, il adaucam ca cheie si creem un dictonar pentru valorile lui
                    if data[1] not in structura_fisier[sectiune_curenta][data[0]]:
                        structura_fisier[sectiune_curenta][data[0]][data[1]] = [] # Adaugam o lista in care se vor salva starile in care se duce starea curenta pentru input ul curent

                    structura_fisier[sectiune_curenta][data[0]][data[1]].append(data[2]) # Adaugam starile in care se duce starea curenta in lista

                else:
                    structura_fisier[sectiune_curenta].append(data)

    return structura_fisier


def verificare_corectitudine_sigma(structura):
    if 'Sigma' not in structura:
        print("Nu exista alfabetul")
        return False

    elif len(structura['Sigma']) == 0:  # Verific daca sectiunea este goala
        print("Sectiunea Sigma este goala")
        return False

    else:

        if sorted(structura['Sigma']) != sorted(
                list(set(structura['Sigma']))):  # Verific unicitatea elementelor din limbaj
            print("Alfabetul nu are elemente unice")
            return False

    return True


def verificare_corectitudine_States(structura):
    if 'States' not in structura:
        print("Nu exista States")
        return False

    elif len(structura['States']) == 0:  # Verific daca sectiunea States este sau nu goala
        print("Sectiunea States este goala")
        return False

    else:

        # Verific daca exista o stare initiala si cel putin o stare finala

        exista_stare_finala = False
        exista_stare_initiala = False

        for element in structura['States']:
            componente = element.split(
                ", ")  # Impart elementul pe componente pentru a putea fi verificate regulile mai usor
            numar_componente = len(componente)
            if numar_componente == 2:
                if componente[1] == 's':  # Verific daca am gasit o stare initiala
                    if exista_stare_initiala is True:  # Verific daca a mai fost gasita o stare initiala inainte
                        print(
                            "Exista mai multe stari initiale")  # In caz afirmativ afisez o eroare ( poate exista o singura stare initiala )
                        return False
                    else:
                        exista_stare_initiala = True
                else:
                    if componente[1] == 'f':  # Verific daca exista o stare finala
                        exista_stare_finala = True
            elif numar_componente == 3:  # Verific daca e posibil ca starea curenta sa fie initiala sau finala
                if componente[1] == 's':
                    if exista_stare_initiala is True:
                        print("Exista mai multe stari initiale")
                        return False
                    else:
                        exista_stare_initiala = True
                if componente[1] == 'f':
                    exista_stare_finala = True

        if exista_stare_finala is not True or exista_stare_initiala is not True:
            print("Nu exista stari initiale sau finale")
            return False

    return True


def verificare_corectitudine_Actions(structura):
    if 'Actions' not in structura:  # Verific daca exista Actions ca sectiune in fisierul de configuratie
        print("Nu exista sectiunea Actions")
        return False

    elif len(structura['Actions']) == 0:  # Verific daca functia de tranzitie e goala sau nu
        print("Sectiunea Actions este goala")
        return False

    # Verific daca datele din actions sunt corecte, mai exact daca cele trei elemente trimise pe cate o linie apartin sectiunii
    # States ( primul element si al treilea ) si sectiunii Sigma ( elementul din mijloc )

    states = [x[0:2] for x in
              structura['States']]  # Salvez doar starile intr-o variabila separata pentru a fi mai usor de accesat

    for action in structura['Actions']:
        if action not in states:  # Verific daca starea apartine multimii de stari
            print("Datele din Actions nu sunt corecte")
            return False
        for inputStr in structura['Actions'][action]:  # Verific daca input ul recunoscut de starea curenta exista in limbaj
            if inputStr not in structura['Sigma']:
                print("Datele din Actions nu sunt corecte")
                return False
            for actions2 in structura['Actions'][action][inputStr]:  # Verific daca starea apartine multimii de stari
                if actions2 not in states:
                    print("Datele din Actions nu sunt corecte")
                    return False

        # Verific daca functia pentru tranzitii contine elemente corecte

    return True


def verificare_corectitudine_fisier(structura):
    corect_Sigma = verificare_corectitudine_sigma(structura)

    if corect_Sigma is False:
        return False

    corect_States = verificare_corectitudine_States(structura)

    if corect_States is False:
        return False

    corect_Actions = verificare_corectitudine_Actions(structura)

    if corect_Actions is False:
        return False

    return True


def determinare_stari_initiala_finala(dfa):
    stare_initiala = 0
    stari_finale = []

    for stare in dfa['States']:
        componente = stare.split(", ")  # Impart string ul pe componente pentru a fi mai usor de verificat conditiile
        numar_componente = len(componente)

        if numar_componente > 1:  # Verific se dau mai multe informatii despre starea curenta
            if componente[1] == 's':
                stare_initiala = componente[0]
                if numar_componente == 3:  # Verific daca starea curenta poate fi si initiala si finala
                    if componente[2] == 'f':
                        stari_finale.append(componente[0])
            elif componente[1] == 'f':
                stari_finale.append(componente[0])


    return stare_initiala, stari_finale


def emulate_dfa(dfa, sir_input, stare_inceput, stari_finale):
    stari_curente = [stare_inceput]  # Pun starile asupra carora se va aplica input ul in aceasta variabila
    stari_viitoare = []  # Aici voi pune starile care urmeaza sa fie procesate dupa ce sunt procesate cele curente

    for c in sir_input:  # Iau fiecare caracter din input
        if c not in dfa['Sigma']:  # Daca caracterul pe care il citesc nu se afla in limbaj, afisez o eroare
            print("Sirul nu este recunoscut de automat")
            return False

        for stare in stari_curente:  # Verific daca de la starea curenta mai exista tranzitii
            if 'e' in dfa['Actions'][stare]:
                stari_viitoare.extend(dfa['Actions'][stare]['e'])
            if c in dfa['Actions'][stare]:  # Verific daca din starea curenta se mai poate ajunge in alte stari cu input ul curent
                stari_viitoare.extend(dfa['Actions'][stare][c])  # In caz afirmativ, extind lista de stari viitoare cu starile la care se poate ajunge din starea curenta cu input ul curent pentru a fi procesate la pasul urmator

        stari_curente = set(stari_viitoare)  # Starile viitoare sunt puse in lista de stari curente pentru a fi procesate la pasul urmator
        stari_viitoare = []

    for stare in stari_curente:
        if stare in stari_finale:  # Verific daca macar una dintre starile la care am ajuns se afla in multimea de stari finale
            return True

    return False  # In cazul in care printre starile la care am ajuns nu se afla nicio stare finala, inseamna ca automatul nu a acceptat input ul


def start_app():
    nume_fisier = "date.in"  # Citesc numele fisierului in care se afla configuratia
    date_fisier = citire_fisier(nume_fisier)  # Colectez toate informatiile din fisier in aceasta variabila

    if date_fisier is not None:
        structura_fisier = file_parser(date_fisier)  # Structurez informatiile pe sectiuni intr un dictionar

        if structura_fisier is not False:

            if verificare_corectitudine_fisier(structura_fisier):  # Verific daca datele primite sunt corecte


                stare_init, stari_fin = determinare_stari_initiala_finala(structura_fisier)

                secventa = citire_secventa()  # Citesc inputul care urmeaza sa fie procesat

                print(emulate_dfa(structura_fisier, secventa, stare_init,stari_fin))  # Afisez daca secventa a fost sau nu acceptata de automat


start_app()  # Functia care porneste automatul si citirea fisierului de configuratie



#TODO:  WARNING: Merge doar pentru o singura variabila