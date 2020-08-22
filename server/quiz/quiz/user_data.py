from collections import Counter

from quiz import spotify
from quiz.quiz.utils import *

class UserData:
    def __init__(self, session):
        self.session = session
        self.time_ranges = ['long_term', 'medium_term', 'short_term']

        self._music_taste = None
        self._playlists = None
        self._recently_played = None
        self._saved_tracks = None
        self._saved_albums = None
        self._followed_artists = None
        self._top_artists = {}
        self._top_tracks = {}
        self._top_genres = {}
        self._personal_data = None


    def personal_data(self):
        if not self._personal_data:
            self._compile_personal_data()
        return self._personal_data


    def music_taste(self):
        if not self._music_taste:
            self._compile_music_taste()
        return self._music_taste


    def music_taste_with_audio_features(self):
        if not self._music_taste:
            self._compile_music_taste()
        if not self._music_taste[0].get('energy'):
            self._compile_audio_features()
        return self._music_taste


    def playlists(self):
        if not self._playlists:
            self._compile_playlists()
        return self._playlists


    def playlists_detailed(self):
        if not self._playlists:
            self._compile_playlists()
        if self._playlists and not self._playlists[0].get('followers'):
            self._compile_playlist_details()
        return self._playlists


    def recently_played(self):
        if not self._recently_played:
            self._compile_recently_played()
        return self._recently_played


    def top_artists(self, time_range):
        if not self._top_artists or not self._top_artists.get(time_range):
            self._compile_top_artists(time_range)
        return self._top_artists.get(time_range)


    def top_tracks(self, time_range):
        if not self._top_tracks or not self._top_tracks.get(time_range):
            self._compile_top_tracks(time_range)
        return self._top_tracks.get(time_range)


    def top_genres(self, time_range):
        if not self._top_genres or not self._top_genres.get(time_range):
            self._compile_top_genres(time_range)
        return self._top_genres.get(time_range)

    
    def saved_tracks(self):
        if not self._saved_tracks:
            self._compile_saved_tracks()
        return self._saved_tracks

    
    def saved_albums(self):
        if not self._saved_albums:
            self._compile_saved_albums()
        return self._saved_albums


    def followed_artists(self):
        if not self._followed_artists:
            self._compile_followed_artists()
        return self._followed_artists


    def get_playlist_with_tracks(self, playlist_id):
        playlists = self.playlists()

        playlist = None
        for p in playlists:
            if p['id'] == playlist_id:
                playlist = p
                break

        if not playlist:
            return False

        url = '/v1/playlists/' + playlist_id
        query_dict = { 'fields': 'tracks' }
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        non_destructive_update(playlist, results.json())

        self._playlists = playlists
        return playlist



    def _compile_music_taste(self):
        long_top_tracks = self.top_tracks('long_term')
        medium_top_tracks = self.top_tracks('medium_term')
        short_top_tracks = self.top_tracks('short_term')

        all_results = long_top_tracks + medium_top_tracks + short_top_tracks

        # Turn results into a dictionary, where the key is a track's id, and the
        # item is the track JSON itself. This removes track items with duplicate
        # ids. Then turn the dict values into a list, which is a list of unique
        # tracks
        self._music_taste = list({t['id']:t for t in all_results}.values())


    def _compile_playlists(self):
        playlists = []

        limit = 50
        query_dict = {'limit': limit}
        url = '/v1/me/playlists'
        page = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        json = page.json()
        playlists.extend(json['items'])
        while(json.get('next')):
            page = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = page.json()
            playlists.extend(json['items'])

        self._playlists = playlists

    
    def _compile_saved_tracks(self):
        saved_tracks = []

        limit = 50
        query_dict = { 'limit': limit }
        url = '/v1/me/tracks'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        json = results.json()
        for i in json['items']:
            saved_tracks.append(i['track'])
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            for i in json['items']:
                saved_tracks.append(i['track'])

        self._saved_tracks = saved_tracks

    
    def _compile_saved_albums(self):
        saved_albums = []

        limit = 50
        query_dict = { 'limit': limit }
        url = '/v1/me/albums'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        json = results.json()
        for i in json['items']:
            saved_albums.append(i['album'])
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            for i in json['items']:
                saved_albums.append(i['album'])

        self._saved_albums = saved_albums


    def _compile_followed_artists(self):
        followed_artists = []

        limit = 50
        query_dict = {
            'limit': limit,
            'type': 'artist' 
        }
        url = '/v1/me/following'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        json = results.json()
        followed_artists.extend(json['artists']['items'])
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            followed_artists.extend(json['items'])

        self._followed_artists = followed_artists


    def _compile_recently_played(self):
        limit = 50
        query_dict = {'limit': limit}
        url = '/v1/me/player/recently-played'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        self._recently_played = [t['track'] for t in results.json()['items']]


    def _compile_top_tracks(self, time_range):
        limit = 50
        query_dict = {
            'limit': limit,
            'time_range': time_range
        }
        url = '/v1/me/top/tracks'

        long_results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        self._top_tracks[time_range] = long_results.json()['items']


    def _compile_top_artists(self, time_range):
        limit = 50
        query_dict = {
            'limit': limit,
            'time_range': time_range
        }
        url = '/v1/me/top/artists'

        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        self._top_artists[time_range] = results.json()['items']


    def _compile_top_genres(self, time_range):
        top_artists = self.top_artists(time_range)

        # Get list of all genres
        top_genres = [a['genres'] for a in top_artists]

        self._top_genres[time_range] = top_genres


    def _compile_personal_data(self):
        url = '/v1/me'
        results = spotify.make_authorized_request(self.session, url)

        self._personal_data = results.json()


    def _compile_audio_features(self):
        music_taste = self.music_taste() 

        ids = [t['id'] for t in music_taste]

        limit = 100
        id_sections = split_into_subsections(ids, limit)
        for section in id_sections:
            url = '/v1/audio-features'
            query_dict = { 'ids': spotify.create_id_querystr(section) }
            results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

            tracks = results.json()['audio_features'] 

            music_taste = combine_track_json(music_taste, tracks)

        self._music_taste = music_taste


    def _compile_playlist_details(self):
        playlists = self.playlists()

        for p in playlists:
            url = '/v1/playlists/' + p['id']
            query_dict = { 'fields': 'followers' }
            results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
            p['followers'] = results.json()['followers']

        self._playlists = playlists 
