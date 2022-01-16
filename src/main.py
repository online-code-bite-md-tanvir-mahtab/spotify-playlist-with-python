# importing all the module and library
from ast import If
from turtle import position
from unicodedata import name
from urllib import request
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth



user_inputed_date = input("Enter you date like this formate : YYYY-mm-dd:")

# Constant
URL_OF_THE_WEB = f"https://www.billboard.com/charts/hot-100/{user_inputed_date}/"
# url of the spotify url
SPOTIFY_URL = 'http://127.0.0.1:8080'
# sending requst for the web to the server
response = requests.get(url=URL_OF_THE_WEB)
SCOPE = 'playlist-modify-private'
CLIENT_ID = 'a5025d451c924a34b812532231019c9a'
CLIENT_SECTET = '1f6bc1342bd44bb6acb8a03b0857203b'



# checking and trigaring the error if something goes wrong
# print(response.status_code)
response.raise_for_status

data = response.text

# now i am going to create the instance of the beautifusoup class
soup = BeautifulSoup(data,'html.parser')


# now i am going to find the specific element
# song_title = soup.find_all(name='a',class_="c-title__link lrv-a-unstyle-link")
# song_title = soup.find_all(name="li", class_="o-chart-results-list__item // lrv-u-background-color-black lrv-u-color-white u-width-100 u-width-55@mobile-max u-width-55@tablet-only lrv-u-height-100p lrv-u-flex lrv-u-flex-direction-column@mobile-max lrv-u-flex-shrink-0 lrv-u-align-items-center lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey")
song_title = [songs.getText().split("\n")[1] for songs in soup.find_all("h3",class_="c-title")]
list_of_songs = []
final_list_of_song = []
# print(song_title)
count = 0
for item in range(len(song_title)):
    # if item == 'Songwriter(s):' and item == 'Producer(s):' and item == 'Imprint/Promotion Label:':
    #     # song_title.remove(item)
    #     print("found")
    # print(item,"->",song_title[item])
    list_of_songs.append(song_title[item])


# print(list_of_songs)
for songs in list_of_songs:
    if list_of_songs[0] == songs or list_of_songs[1] == songs or list_of_songs[2]==songs or list_of_songs[3]== songs:
        pass
    else:
        final_list_of_song.append(songs)





# creating the authintication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri=SPOTIFY_URL ,client_id=CLIENT_ID,client_secret=CLIENT_SECTET,scope=SCOPE))


USER_ID  = sp.current_user()['id']

new_song_id = []
new_song_name = []
for song in final_list_of_song:
    year = user_inputed_date.split('-')[0]
    result = sp.search(q=f"track: {song} year: {year}",limit=10,type='track')
    # print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_name = result['tracks']['items'][0]['name']
        print(f'the uri : {uri}')
        new_song_id.append(uri)
        new_song_name.append(song_name)
    except IndexError:
        # print(f"{song} dosen't exist in the list")
        pass


# now creating new playlist
paly_list_name = user_inputed_date

playlist = sp.user_playlist_create(user=USER_ID,name=f"{paly_list_name} Billboard 100",public=False,collaborative=True)


print(playlist['id'])
# print(new_song_uri)
# sp.playlist_add_items(playlist_id=playlist['id'],items=new_song_id,position=None)
dno = sp.user_playlist_add_tracks(user=USER_ID,playlist_id=playlist['id'],tracks=new_song_id[0:6],position=None)
print(dno)
play_list_of_user = sp.user_playlist(user=USER_ID,playlist_id=playlist['id'])
print(play_list_of_user)

