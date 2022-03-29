import PySimpleGUI as sg
import mysql.connector
mydb = mysql.connector.connect(
    host="145.74.104.145",
    user="eldok",
    password="Aa637277!",
    database="blok3"
)


sg.theme('Dark')
layout = [[sg.Text("Welcome to Spotipy, THE shoddy music app for YOU.")],
          [sg.Text("Click what you want to do next")],
          [sg.Button("Enter a song"), sg.Button("Select an album"),
           sg.Button("Search for a song"), sg.Button("Artist information")],
          [sg.Exit()]]
window = sg.Window("Spotipy", layout, element_justification='c')


def enter_song():
    album_cursor = mydb.cursor()
    album_cursor.execute("select * from album")
    album_name_list = []
    album_id_list = []
    for album in album_cursor:
        album_name_list.append(album[1])
        album_id_list.append(album[0])
    output = []
    song_layout = [
        [sg.Text("Enter a the title of the song")],
        [sg.InputText(key='TITLE')],
        [sg.Text("The duration of the song as follows: 00:00:00")],
        [sg.InputText(key='DURATION')],
        [sg.Text("Enter a YouTube Link")],
        [sg.InputText(key='LINK')],
        [sg.Text("Select an album")],
        [sg.Listbox(album_name_list, key='_ALBUM_LIST_',
                    size=(30, 8))],
        [sg.Text("Output")],
        [sg.Listbox(output, key='OUTPUT', size=(45, 1))],
        [sg.Button("OK"), sg.Button("CANCEL")]
    ]
    song_window = sg.Window("Song entering menu", song_layout,
                            enable_close_attempted_event=True)
    while True:
        event, values = song_window.read()
        song_title = song_window['TITLE'].get()
        song_duration = song_window['DURATION'].get()
        youtube = song_window['LINK'].get()
        album_id_query = "select id from album where title like %s"
        album_tuple = (values['_ALBUM_LIST_'][0],)
        album_cursor.execute(album_id_query, album_tuple)
        for x in album_cursor:
            album_id = x
        if event is None or event == 'CANCEL' or event == sg.WINDOW_CLOSED:
            song_window.close()
            return
        if event == 'OK' and song_title and song_duration and album_id:
            song_enter_query = "INSERT INTO muzieknummers(title, duration," \
                               " youtube_link, album_id)" \
                               " VALUES (%s, %s, %s, %s)"
            song_tuple = (song_title, song_duration, youtube, album_id[0])
            song_selector = mydb.cursor()
            try:
                song_selector.execute(song_enter_query, song_tuple)
                mydb.commit()
                output.append("Added song")
                song_window['OUTPUT'].update(output)
            except:
                mydb.rollback()
                output.append("Couldn't add song, try again.")
                song_window['OUTPUT'].update(output)


def album_select():
    album_select_cursor = mydb.cursor()
    album_select_cursor.execute("select * from album")
    album_name_list = []
    songs = []
    for album in album_select_cursor:
        album_name_list.append(album[1])
    album_select_layout = [
        [sg.Text("Pick the album you wish to see the songs from")],
        [sg.Listbox(album_name_list, key='_ALBUM_LIST_',
                    size=(30, 8)
                    )],
        [sg.Listbox(songs, size=(60, 15), key='OUTPUT')],
        [sg.Button("CONFIRM"), sg.Button("CANCEL")]
    ]
    album_selection_window = sg.Window("Album song selection menu",
                                       album_select_layout)
    while True:
        event, values = album_selection_window.read()
        album_id_query = "select id from album where title like %s"
        album_tuple = (values['_ALBUM_LIST_'][0],)
        album_select_cursor.execute(album_id_query, album_tuple)
        for x in album_select_cursor:
            album_id = (x)
        song_query = "select title from muzieknummers where album_id = %s"
        album_select_cursor.execute(song_query, album_id)
        for x in album_select_cursor:
            songs.append(x)
        if event is None or event == 'CANCEL' or event == sg.WINDOW_CLOSED:
            album_selection_window.close()
            return
        if event == "CONFIRM":
            album_selection_window['OUTPUT'].update(songs)
            songs = []


def song_search():
    song_return_list = []
    song_search_layout = [
        [sg.Text("Search for any song in the database")],
        [sg.InputText(key="SONG")],
        [sg.Button("CONFIRM"), sg.Button("CANCEL")],
        [sg.Listbox(song_return_list, size=(60, 15), key='OUTPUT')]
    ]
    song_search_cursor = mydb.cursor()
    song_search_window = sg.Window("Song Searching Menu", song_search_layout)
    song_query = "select title from muzieknummers where title like %s"
    while True:
        event, values = song_search_window.read()
        if event is None or event == 'CANCEL' or event == sg.WINDOW_CLOSED:
            song_search_window.close()
            return
        if event == "CONFIRM":
            args = ['%' + values['SONG'] + '%']
            song_search_cursor.execute(song_query, args)
            for x in song_search_cursor:
                song_return_list.append(x)
                song_search_window["OUTPUT"].update(song_return_list)
            song_return_list = []


def artist_search():
    artist_cursor = mydb.cursor()
    artist_cursor.execute("select * from album")
    album_name_list = []
    artist_information = []
    for album in artist_cursor:
        album_name_list.append(album[1])
    artist_layout = [
        [sg.Text("Pick an album you wish to see the artist's information of")],
        [sg.Listbox(album_name_list, key='_ALBUM_LIST_', size=(30, 8))],
        [sg.Text("Artist Informaton")],
        [sg.Button("CONFIRM"), sg.Button("CANCEL")],
        [sg.Listbox(artist_information, key="OUTPUT", size=(30, 1))]
    ]
    artist_window = sg.Window("Artist Information Menu", artist_layout)
    artist_query = "select * from artiest where id =" \
                   " (select artiest_id from album where title like %s)"
    while True:
        event, values = artist_window.read()
        album_tuple = (values['_ALBUM_LIST_'][0],)
        artist_cursor.execute(artist_query, album_tuple)
        for info in artist_cursor:
            artist_information.append(info)
        if event is None or event == "CANCEL" or event == sg.WINDOW_CLOSED:
            artist_window.close()
            return
        if event == "CONFIRM":
            print("test")
            artist_window["OUTPUT"].update(artist_information)
            artist_information = []


while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == 'Enter a song':
        enter_song()
        continue
    if event == 'Select an album':
        album_select()
        continue
    if event == 'Search for a song':
        song_search()
        continue
    if event == 'Artist information':
        artist_search()
        continue


window.close()
