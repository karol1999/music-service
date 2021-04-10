import pymysql

# ustanowienie połączenia z bazą danych
connection = pymysql.Connection(
    host = 'localhost',
    user = 'root',
    db = 'serwis_muzyczny',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

# funkcja potrzebna do zebrania wszystkich haseł oraz loginów (potrzebna do logowania)
def getAllLoginsAndPasswords():
    with connection.cursor() as object:
        SQL = "SELECT user.login, user.password FROM user"
        object.execute(SQL)
        allLoginsAndPasswords = object.fetchall() # fetchone() -> bierze jeden wiersz
        return allLoginsAndPasswords

# funkcja potrzebna do zebrania wszystkich loginów (potrzebna do rejestracji)
def getAllLogins():
    with connection.cursor() as object:
        SQL = "SELECT user.login FROM user"
        object.execute(SQL)
        allLogins = object.fetchall() # fetchone() -> bierze jeden wiersz
        return allLogins

# funkcja potrzebna do zapisania danych nowo zarejestrowanego użytkownika (potrzebna do rejestracji)
def writeToDatabase(login_, imie_, nazwisko_, haslo_):
    with connection.cursor() as object:
        SQL = "INSERT INTO user (login, name, surname, password) VALUES (%s, %s, %s, %s)"
        values = (login_, imie_, nazwisko_, haslo_)
        object.execute(SQL, values)
        connection.commit()

# usuwanie podanego użytkownika z bazy danych
def deleteUser(login_):
    with connection.cursor() as object:
        SQL = "DELETE FROM user WHERE login = \"" + login_ + "\""
        object.execute(SQL)
        connection.commit()


# szukanie piosenek i wyświetlanie
def searchForSongs(searchInput_):
    with connection.cursor() as object:
        SQL = "SELECT song.song_id, artist.name, song.title, album.name, album.year, song.likes_count, genre.name FROM song INNER JOIN artist ON song.artist_id=artist.artist_id INNER JOIN album ON song.album_id=album.album_id INNER JOIN genre ON song.genre_id=genre.genre_id WHERE song.title=%s OR artist.name=%s OR album.name=%s OR genre.name=%sORDER BY song.song_id"
        values = (searchInput_, searchInput_, searchInput_, searchInput_)
        object.execute(SQL, values)
        searchResult = object.fetchall()
        return searchResult

# wyświetla listę polubionych artystów danego użytkownika
def getAllLikedArtists(loggedUserLogin_):
    with connection.cursor() as object:
        SQL = "SELECT artist.artist_id, artist.name FROM liked_artist INNER JOIN artist ON liked_artist.artist_id=artist.artist_id WHERE liked_artist.login=\"" + loggedUserLogin_ + "\" ORDER BY artist.name"
        object.execute(SQL)
        allLikedArtists = object.fetchall()
        return allLikedArtists

# wyswietl wszystkie polubione piosenki uzytkownika
def getAllLikedSongs(loggedUserLogin_):
    with connection.cursor() as object:
        SQL = "SELECT liked_song.song_id, artist.name, song.title, album.name, album.year, genre.name FROM liked_song INNER JOIN song ON liked_song.song_id=song.song_id INNER JOIN artist ON song.artist_id=artist.artist_id INNER JOIN album ON song.album_id=album.album_id INNER JOIN genre ON song.genre_id=genre.genre_id WHERE liked_song.login=\"" + loggedUserLogin_ + "\" ORDER BY song.song_id"
        object.execute(SQL)
        allLikedSongs = object.fetchall()
        return allLikedSongs

# pobiera dane piosenki, która jest aktualnie odtwarzana
def getSongById(playingSongId_):
    with connection.cursor() as object:
        SQL = "SELECT song.song_id, artist.name, song.title, album.name, album.year, song.likes_count, genre.name FROM song INNER JOIN artist ON song.artist_id=artist.artist_id INNER JOIN album ON song.album_id=album.album_id INNER JOIN genre ON song.genre_id=genre.genre_id WHERE song.song_id=" + str(playingSongId_)
        object.execute(SQL)
        songDetails = object.fetchone()
        return songDetails

# wyświetla pozostałe piosenki z aktualnie odtwarzanej playlisty
def getAllPlaylistSongs(playingPlaylistName_, playingSongId_):
    with connection.cursor() as object:
        SQL = "SELECT playlist.song_id, artist.name, song.title FROM song INNER JOIN playlist ON playlist.song_id=song.song_id INNER JOIN artist ON song.artist_id=artist.artist_id WHERE playlist.name=%s AND playlist.song_id!=%s"
        values = (playingPlaylistName_, str(playingSongId_))
        object.execute(SQL, values)
        playingPlaylistSongs = object.fetchall()
        return playingPlaylistSongs

# usuwanie piosenki z listy ulubionych piosenek
def deleteFromLikedSongs(songId_, loggedUserLogin_):
    with connection.cursor() as object:
        SQL = "UPDATE song SET song.likes_count = song.likes_count - 1 WHERE song.song_id=" + songId_
        object.execute(SQL)
        connection.commit()
        SQL = "DELETE FROM liked_song WHERE liked_song.song_id = %s AND liked_song.login = %s"
        values = (songId_, loggedUserLogin_)
        object.execute(SQL, values)
        connection.commit()

# dodanie piosenki do listy polubionych piosenek oraz zwiekszenie liczby polubien o jeden (tej piosenki)
def addToLikedSongs(songId_, loggedUserLogin_):
    with connection.cursor() as object:
        SQL = "INSERT INTO liked_song (login, song_id) SELECT %s, song.song_id FROM song WHERE song.song_id = %s"
        values = (loggedUserLogin_, songId_)
        object.execute(SQL, values)
        connection.commit()
        SQL = "UPDATE song SET song.likes_count = song.likes_count + 1 WHERE song.song_id=" + str(songId_)
        object.execute(SQL)
        connection.commit()

# usuniecie artysty z listy polubionych artystów
def deleteFromLikedArtist(idOfAnArtist, login_):
    with connection.cursor() as object:
        SQL = "DELETE FROM liked_artist WHERE liked_artist.artist_id = %s AND liked_artist.login = %s"
        values = (str(idOfAnArtist), login_)
        object.execute(SQL, values)
        connection.commit()



# zrobic tak żeby użytkownik nie polubił tej samej piosenki dwa razy