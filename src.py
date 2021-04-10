# menu
from termcolor import colored   # do kolorowania składni
import sys                      #
import database                 # import zapytań bazy danych

class Menu:

    witaj = "Witaj w bibliotece muzycznej!!!"

    menu = """
    Wybierz 1 gdy chcesz sie zalogowac
    Wybierz 2 gdy chcesz sie zarejestrowac
    Wybierz 3 gdy chcesz wyjsc 
    Twoj wybor to: """

    menuZalogowanegoUzytkownika = """
    Zalogowales sie do systemu. Co chcialbys zrobic?
    Wpisz:
    1 - do wyszukania piosenki
    2 - do wyszukania polubionych piosenek
    3 - do wyszukania polubionych artystow
    4 - do wyjscia z programu
    5 - usuniecie konta
    6 - zmiana uzytkownika 
    """

    # potrzebne do trzymania loginu zalogowanego uzytkownika +/- cos takiego ja identyfikator
    loginZalogowanegoUzytkownika = None
    aktualnieOdtwarzanaPiosenka = None
    aktualnaPlaylista = None

    def callMenu(self):

        print() # dla przejrzystości
        print(" \t", self.witaj) # przywitanie sie z użytkownikiem

        while True: # nieskończona pętla po to aby użytkownik cały czas miał menu przed sobą, żeby wyjść z niego
                    # trzeba wybrać odpowiedni numer

            wyborUzytkownika = int(input(self.menu)) # użytkownik wybiera co chce zrobć

            if wyborUzytkownika == 1: #logowanie
                print()
                login = input("\tPodaj swoj login: ")
                haslo = input("\tPodaj swoje haslo: ")

                # sprawdzenie czy uzytkownik podaje dobre haslo i login podczas logowania i logowanie (czyli wyswietlene menu dla zalogowanego konsumenta)
                for uzytkownik in database.getAllLoginsAndPasswords():
                    if login == uzytkownik["login"] and haslo == uzytkownik["password"]:
                        print(colored("\tUdalo sie poprawnie zalogowac", 'green'))
                        self.loginZalogowanegoUzytkownika = login # do ewentualnego usuniecia konta
                        print("\n" * 50) # czyszczenie ekranu DO POPRAWY
                        self.callMenuZalogowane(self) # wyswietlnie menu dla zalogowanego konsumenta
                    else:
                        print(colored("\tNiestety podales zly login", 'red')) # wrocenie na sam początek

            elif wyborUzytkownika == 2: #rejestracja
                print()
                imie = input("\tPodaj swoje imie: ")
                nazwisko = input("\tPodaj swoje nazwisko: ")
                login = input("\tPodaj swoj login: ")
                haslo = input("\tPodaj swoje haslo: ")

                #
                for uzytkownik in database.getAllLogins():
                    if login == uzytkownik["login"]:
                        print(colored("\tNiestety uzytkownik o podanej nazwie juz istnieje", 'red'))
                        break
                    elif login != uzytkownik["login"]:
                        print(colored("\tUdalo sie zarejestrowac", 'green'))
                        self.loginZalogowanegoUzytkownika = login # do ewentualnego usuniecia konta
                        database.writeToDatabase(login, imie, nazwisko, haslo)
                        print("\n" * 50) # czyszczenie ekranu DO POPRAWY
                        self.callMenuZalogowane(self)

            elif wyborUzytkownika == 3: #exit
                print("\tZamykanie systemu...")
                exit()
            else: #zly wybor
                print(colored("\tWybrales niewlasciwa opcje", 'red'))

##############################################################################################################################################

    def callMenuZalogowane(self): # po pomyślnym zalogowaniu tudzież rejestracji odpala się to menu

        print() # dla lepszej przejrzystości

        while True: # nieskończona pętla po to aby użytkownik cały czas miał menu przed sobą, żeby wyjść z niego
                    # trzeba wybrać odpowiedni numer

            wyborUzytkownika = int(input(self.menuZalogowanegoUzytkownika)) # wybor użytkownika co chce robić

            if wyborUzytkownika == 1: # szukanie piosenki (zapytanie do bazy wyswietla piosenkę i jej szczegóły)
                                      # otherwise error
                wybor = input("Wyszukiwana fraza: ") # album, artysta, nazwa piosenki trzeba dobrze napisac
                                                     # ponieważ inczej nie znajdzie DO POPRAWY
                print("\n"*50)                       # czyszczenie command prompta DO POPRAWY
                sprawdzCzyBylJakisOdzew = 0
                for song in database.searchForSongs(wybor):
                    print("Znaleziono utwor nalezacy do playlisty " + song['genre.name'])
                    print("wykonawca: " + song['name'])
                    self.aktualnieOdtwarzanaPiosenka = song['song_id']
                    self.aktualnaPlaylista = song['genre.name']
                    print("tytul: " + song['title'])
                    print("album: " + song['album.name'])
                    print("rok wydania: " + str(song['year']))
                    print("liczba polubien: " + str(song['likes_count']))
                    sprawdzCzyBylJakisOdzew = 1
                    break
                if sprawdzCzyBylJakisOdzew == 0:
                    print(colored("Brak wynikow", 'red'))

                print("Co chcialbys zrobic z piosenka? 1 - SLUCHAJ, 2 - KONTYNUUJ")
                wybor = input("Twoj wybor: ")

                if wyborUzytkownika == 1: # Słuchanie danej piosenki z opcja polubienia
                    print("\n" * 50)
                    print("Aktualnie odtwarzana piosenka: ")
                    playingSong = database.getSongById(self.aktualnieOdtwarzanaPiosenka)
                    print("wykonawca: " + playingSong['name'])
                    print("tytul: " + playingSong['title'])
                    print("liczba polubien: " + str(playingSong['likes_count']))
                    print()
                    print("Pozostale piosenki w playliscie:")
                    print("id\twykonawca\ttytul")
                    for playlistSongs in database.getAllPlaylistSongs(self.aktualnaPlaylista, self.aktualnieOdtwarzanaPiosenka):
                        print(str(playlistSongs['song_id']) + "\t" + playlistSongs['name'] + "\t" + playlistSongs['title'])

                    print("Co chcesz zrobic? 1 - DODANIE PIOSENKI DO ULUBIONYCH, 2 - PRZEJSCIE DO SLUCHANIA KOLEJNEJ PIOSENKI, 3 - WYJSCIE")
                    wybor = int(input("Twoja decyzja: "))

                    if wybor == 1: # dodanie do ulubionych
                        database.addToLikedSongs(str(self.aktualnieOdtwarzanaPiosenka), self.loginZalogowanegoUzytkownika)
                        print("Dodano utwor do ulubionych")
                        print("\n" * 50) # wyczyszczenie okna po dodaniu do ulubionych

                        ###############################################################

                        print("Aktualnie odtwarzana piosenka: ")
                        playingSong = database.getSongById(self.aktualnieOdtwarzanaPiosenka)
                        print("wykonawca: " + playingSong['name'])
                        print("tytul: " + playingSong['title'])
                        print("liczba polubien: " + str(playingSong['likes_count']))
                        print()
                        print("Pozostale piosenki w playliscie:")
                        print("id\twykonawca\ttytul")
                        for playlistSongs in database.getAllPlaylistSongs(self.aktualnaPlaylista, self.aktualnieOdtwarzanaPiosenka):
                            print(str(playlistSongs['song_id']) + "\t" + playlistSongs['name'] + "\t" + playlistSongs[
                                'title'])

                        print("Co chcesz zrobic? 1 - PRZEJSCIE DO SLUCHANIA KOLEJNEJ PIOSENKI, 2 - WYJSCIE")
                        wybor = input("Twoja decyzja to 2: ")
                        wybor = 2 # XD

                elif wybor == 2: # powrot do menu
                    print("\tPowrot do menu...")
                else:
                    print("\tNiepoprawny wybor")
                #if piosenke_znaleziono
                    #kolejny if co chcesz z nia zrobic albo posluchac, albo dodac do ulubionych
                    #dodanie do ulubionych
                    #sluchanie (emulacja sluchania piosenki, wyjscie z niej, pauza)
                    #usuniecie z ulubionych
                    #dodanie artysty do plubionych
            elif wyborUzytkownika == 2: # wyświetlenie polubionych piosenek
                print("\n" * 50)
                print("LISTA ULUBIONYCH PIOSENEK")
                print()
                print("id\twykonawca\ttytul\tliczba polubien")
                for likedSong in database.getAllLikedSongs(self.loginZalogowanegoUzytkownika):
                    print(likedSong['song_id'], "\t", likedSong['name'], "\t", likedSong['title'], "\t",
                        likedSong['album.name'], "\t", likedSong['year'], "\t", likedSong['genre.name'])
                    #wylistowanie polubionych piosenek, sluchanie ich, usuniecie z polubionych
                    #wyjscie do menu

                print("Czy chcesz usunac jakiegos piosenke z listy polubionych? 1 - TAK, 2 - NIE")
                wybor = int(input("Twoj wybor: "))

                if wybor == 1:  # usuwamy z listy
                    piosenkaDoUsunieciaID = int(input("ID piosenki do usuniecia: "))
                    database.deleteFromLikedSongs(str(piosenkaDoUsunieciaID), self.loginZalogowanegoUzytkownika)
                    print(colored("Usunieto wybrana piosenke z ulubionych", 'green'))
                elif wybor == 2:
                    print("\n" * 50)
                    pass
                else:
                    print(colored("Niepoprawny wybor", 'red'))

            elif wyborUzytkownika == 3: # wyswietlnie ulubionych artystów użytkownika
                print("\n"*50)
                print("LISTA ULUBIONYCH ARTYSTOW")
                print()
                print("id\twykonawca")

                for artist in database.getAllLikedArtists(self.loginZalogowanegoUzytkownika):
                    print(artist['artist_id'], "\t", artist['name'])

                print("Czy chcesz usunac jakiegos artyste z listy polubionych? 1 - TAK, 2 - NIE")
                wybor = int(input("Twoj wybor: "))

                if wybor == 1: # usuwamy z listy
                    artystaDoUsunieciaID = int(input("ID artysty do usuniecia: "))
                    database.deleteFromLikedArtist(artystaDoUsunieciaID, self.loginZalogowanegoUzytkownika)
                elif wybor == 2:
                    print("\n" * 50)
                    pass
                else:
                    print(colored("Niepoprawny wybor", 'red'))

                #tutaj przeniesienie opcji: usun z listy ulubionych artystow
            elif wyborUzytkownika == 4: # wyjscie z programu (biblioteka muzyczna)
                print("\tWychodzenie z programu...")
                exit()
            elif wyborUzytkownika == 5: # usuniecie konta

                wybor = int(input("\tCzy na pewno chcesz usunac uzytkownika? 1 - TAK, 2 - NIE: "))

                if wybor == 1: # chce usunac konto
                    print("\tUsuwanie uzytkownika...")
                    database.deleteUser(self.loginZalogowanegoUzytkownika)
                    self.callMenu(self)
                elif wybor == 2: # nie chce usuwac
                    print("\tWracanie do menu")
                    break
                else:
                    print("\tNiepoprawny wybor")

            elif wyborUzytkownika == 6: # zmiana uzytkownika
                print("\tPodaj login oraz haslo uzytkownika")
                login = input("\tLogin: ")
                haslo = input("\tHaslo: ")

                # sprawdzenie czy uzytkownik o podanym loginie istnieje i czy haslo jest poprawne
                for uzytkownik in database.getAllLogins():
                    if login == uzytkownik["login"]:
                        print(colored("\tPodany uzytkownik istnieje, zmienianie konta...", 'green'))
                        self.loginZalogowanegoUzytkownika = login  # do ewentualnego usuniecia konta
                        break
                    print(colored("\tUzytkownik o podanej nazwie nie istnieje", 'red'))
            else: # wybranie niewlasciwej opcji i powrot
                print(colored("\tWybrales niewlasciwa opcje", 'red'))

    #def showParticularPlaylist(self):




"""  elif wyborUzytkownika == 3: # wyszukanie ulubionych artystow
#wylistowanie polubionych artystow
#sluchanie ich utworow
#ich albomow
#usuniecie z ulubionych
#powrot
pass """

