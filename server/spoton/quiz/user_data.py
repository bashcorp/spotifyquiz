from collections import Counter

from spoton import spotify

from .utils import *

class UserData:
    """Requests and saves for reuse data from the Spotify API.

    Has functions that request specific data from the Spotify API, and
    saves it so that it doesn't have to be requested again if it's
    needed later.

    All of the data here is a Spotify user's private data, so this
    class needs a Django session with a Spotify user logged in (see
    the spotify module).

    See Also
    --------
    spoton.spotify
    """

    def __init__(self, session):
        """Initializes all data attributes to None, saves user session.

        Initializes all the user's Spotify data attributes to None,
        saves the user session as an attribute. This session must have
        a Spotify user logged in, or no data will be available.

        Parameters
        ----------
        session : django.contrib.sessions.backend.db.SessionStore
            A session object (retrieved from a Django request) with a
            Spotify user logged in (see spoton.spotify module)

        See Also
        --------
        spoton.spotify
        """

        self.session = session

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
        """Returns the Spotify user's personal data as JSON.
        
        Returns the Spotify user's personal data. If it does not exist
        locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's personal data as JSON.

        See Also
        --------
        _compile_personal_data()
        """

        if not self._personal_data:
            self._compile_personal_data()
        return self._personal_data



    def music_taste(self):
        """Returns the Spotify user's music taste data as JSON.
        
        Returns the Spotify user's music taste data. If it does not
        exist locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's music taste data as JSON.

        See Also
        --------
        _compile_music_taste()
        """

        if not self._music_taste:
            self._compile_music_taste()
        return self._music_taste



    def music_taste_with_audio_features(self):
        """Returns the Spotify user's extended music taste data as JSON
        
        Returns the Spotify user's music taste data, with music
        analytic data (happiness, energy, etc.). If it does not exist
        locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's extended music taste data as JSON.

        See Also
        --------
        _compile_audio_features()
        """

        if not self._music_taste:
            self._compile_music_taste()

        # 'energy' is a field that does not in the basic music taste
        # data, so its existance determines whether or not the audio
        # feature data is stored locally
        if self._music_taste[0].get('energy') is None:
            self._compile_audio_features()
        return self._music_taste



    def playlists(self):
        """Returns the Spotify user's simple playlist data as JSON.
        
        Returns the Spotify user's simple playlist data, which does not
        include the tracks in the playlist (for that, use
        get_playlist_with_tracks() ). If it does not exist locally,
        requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's simple playlist data as JSON.

        See Also
        --------
        _compile_playlists()
        """

        if not self._playlists:
            self._compile_playlists()
        return self._playlists



    def playlists_detailed(self):
        """Returns the Spotify user's extended playlist data as JSON.
        
        Returns the Spotify user's extended playlist data, which 
        includes the number of followers of the playlist, but does not
        include the tracks in the playlist. If it does not exist
        locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's extended playlist data as JSON.

        See Also
        --------
        _compile_playlist_details()
        """

        if not self._playlists:
            self._compile_playlists()

        # followers is not given in the basic playlist data, so that
        # existance determines whether or not the extended data is
        # saved locally.
        if self._playlists and self._playlists[0].get('followers') is None:
            self._compile_playlist_details()
        return self._playlists



    def recently_played(self):
        """Returns the Spotify user's recently played tracks as JSON.
        
        Returns the Spotify user's recently played tracks. If it does
        not exist locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's recently played tracks as JSON.

        See Also
        --------
        _compile_recently_played()
        """

        if not self._recently_played:
            self._compile_recently_played()
        return self._recently_played



    def top_artists(self, time_range):
        """Returns the Spotify user's top artist data over a time range
        
        Returns the Spotify user's top artist data as JSON over the
        given time range. If it does not exist locally, requests it
        from the Spotify API.

        Parameters
        ----------
        time_range : str
            The time range over which to return the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.

        Returns
        -------
        dict 
            The Spotify user's top artist data over the time range.

        See Also
        --------
        _compile_top_artists()
        """

        if not self._top_artists or self._top_artists.get(time_range) is None:
            self._compile_top_artists(time_range)
        return self._top_artists.get(time_range)



    def top_tracks(self, time_range):
        """Returns the Spotify user's top track data over a time range
        
        Returns the Spotify user's top track data as JSON over the
        given time range. If it does not exist locally, requests it
        from the Spotify API.

        Parameters
        ----------
        time_range : str
            The time range over which to return the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.

        Returns
        -------
        dict 
            The Spotify user's top track data over the time range.

        See Also
        --------
        _compile_top_tracks()
        """

        if not self._top_tracks or self._top_tracks.get(time_range) is None:
            self._compile_top_tracks(time_range)
        return self._top_tracks.get(time_range)



    def top_genres(self, time_range):
        """Returns the Spotify user's top genre data over a time range
        
        Returns the Spotify user's top genre data as a list over the
        given time range. If it does not exist locally, requests it
        from the Spotify API.

        Parameters
        ----------
        time_range : str
            The time range over which to return the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.

        Returns
        -------
        list 
            The Spotify user's top genre data over the time range.

        See Also
        --------
        _compile_top_tracks()
        """
        if not self._top_genres or self._top_genres.get(time_range) is None:
            self._compile_top_genres(time_range)
        return self._top_genres.get(time_range)

    

    def saved_tracks(self):
        """Returns the Spotify user's saved tracks as JSON.
        
        Returns the Spotify user's saved tracks. If it does
        not exist locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's saved tracks as JSON.

        See Also
        --------
        _compile_saved_tracks()
        """

        if not self._saved_tracks:
            self._compile_saved_tracks()
        return self._saved_tracks

    

    def saved_albums(self):
        """Returns the Spotify user's saved albums as JSON.
        
        Returns the Spotify user's saved albums. If it does
        not exist locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's saved albums as JSON.

        See Also
        --------
        _compile_saved_albums()
        """

        if not self._saved_albums:
            self._compile_saved_albums()
        return self._saved_albums



    def followed_artists(self):
        """Returns the Spotify user's followed artists as JSON.
        
        Returns the Spotify user's followed artists. If it does
        not exist locally, requests it from the Spotify API.

        Returns
        -------
        dict 
            The Spotify user's followed artists as JSON.

        See Also
        --------
        _compile_followed_artists()
        """

        if not self._followed_artists:
            self._compile_followed_artists()
        return self._followed_artists



    def get_playlist_with_tracks(self, playlist_id):
        """Returns the complete playlist data for one playlist as JSON.
        
        Returns the complete data about one of the Spotify user's
        playlists, including the tracks in the playlist. If the data
        does not exist locally, requests it from the Spotify API. The
        playlist id is the Spotify ID (see the Spotify API
        documentation) of that playlist, which must identify a playlist
        that the user owns. If it does not, this function returns None.

        Parameters
        ----------
        playlist_id : str
            The Spotify ID of the playlist to return data about.

        Returns
        -------
        dict 
            The complete data about the playlist.
        """

        # First get basic data about all the user's playlists, so we
        # can ensure that the given playlist id is one of the user's 
        # playlists and not another user's
        playlists = self.playlists()

        playlist = None
        index = None
        for i, p in enumerate(playlists):
            if p['id'] == playlist_id:
                playlist = p
                index = i
                break

        # If no playlist found, fail
        if not playlist:
            return None

        # If playlist isn't one of the user's, fail
        if playlist['tracks'].get('items') is not None:
            return playlist

        # Request the full playlist info
        url = '/v1/playlists/' + playlist_id
        query_dict = { 'fields': 'tracks' }
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        # The simple playlist data has a 'tracks' section that contains
        # the number of tracks and nothing more. Delete that and then
        # merge the dicts

        json = results.json()
        del playlist['tracks']
        json.update(playlist)
        playlists[index] = json # playlist is just a reference, so edit the list

        self._playlists = playlists
        return playlists[index]




    def _compile_music_taste(self):
        """Requests the Spotify user's music taste data and saves it.

        Requests the Spotify user's music taste data and stores it
        locally.
        """

        long_top_tracks = self.top_tracks('long_term')
        medium_top_tracks = self.top_tracks('medium_term')
        short_top_tracks = self.top_tracks('short_term')

        all_results = long_top_tracks + medium_top_tracks + short_top_tracks

        # Turn results into a dictionary, where the key is a track's
        # id, and the item is the track JSON itself. This removes track
        # items with duplicate ids. Then turn the dict values into a
        # list, which is a list of unique tracks
        self._music_taste = list({t['id']:t for t in all_results}.values())



    def _compile_playlists(self):
        """Requests the Spotify user's simple playlist data and saves it.

        Requests the Spotify user's simple playlist data and stores it
        locally.
        """

        playlists = []

        limit = 50
        query_dict = {'limit': limit}
        url = '/v1/me/playlists'

        # Request first page of items
        page = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        json = page.json()
        playlists.extend(json['items'])

        # Keep requesting pages until they run out
        while(json.get('next')):
            page = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = page.json()
            playlists.extend(json['items'])

        self._playlists = playlists

    

    def _compile_saved_tracks(self):
        """Requests the Spotify user's saved tracks and saves them.

        Requests the Spotify user's saved tracks and stores it locally.
        """

        saved_tracks = []

        limit = 50
        query_dict = { 'limit': limit }
        url = '/v1/me/tracks'

        # Get first page of items 
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        json = results.json()
        for i in json['items']:
            saved_tracks.append(i['track'])

        # Get the rest of the pages
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            for i in json['items']:
                saved_tracks.append(i['track'])

        self._saved_tracks = saved_tracks

    

    def _compile_saved_albums(self):
        """Requests the Spotify user's saved albums and saves them.

        Requests the Spotify user's saved albums and stores it locally.
        """

        saved_albums = []

        limit = 50
        query_dict = { 'limit': limit }
        url = '/v1/me/albums'

        # Get first page of items
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        json = results.json()
        for i in json['items']:
            saved_albums.append(i['album'])

        # Get the rest of the pages
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            for i in json['items']:
                saved_albums.append(i['album'])

        self._saved_albums = saved_albums



    def _compile_followed_artists(self):
        """Requests the Spotify user's followed artist data and saves it.

        Requests the Spotify user's followed artist data and stores it
        locally.
        """

        followed_artists = []

        limit = 50
        query_dict = {
            'limit': limit,
            'type': 'artist' 
        }
        url = '/v1/me/following'

        # Get the first page of items
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        json = results.json()
        followed_artists.extend(json['artists']['items'])

        # Get the rest of the pages
        while(json.get('next')):
            results = spotify.make_authorized_request(self.session, json.get('next'), full_url=True)
            json = results.json()
            followed_artists.extend(json['items'])

        self._followed_artists = followed_artists



    def _compile_recently_played(self):
        """Requests the user's recently played tracks and saves them.

        Requests the Spotify user's recently played tracks and stores
        them locally.
        """

        limit = 50
        query_dict = {'limit': limit}
        url = '/v1/me/player/recently-played'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        self._recently_played = [t['track'] for t in results.json()['items']]



    def _compile_top_tracks(self, time_range):
        """Requests the user's top tracks over a period and saves them.

        Requests the Spotify user's top tracks over a time range and
        stores them locally.

        Parameters
        ----------
        time_range : str
            The time range over which to collect the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.
        """

        limit = 50
        query_dict = {
            'limit': limit,
            'time_range': time_range
        }
        url = '/v1/me/top/tracks'

        long_results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        self._top_tracks[time_range] = long_results.json()['items']



    def _compile_top_artists(self, time_range):
        """Requests the user's top artists over a period and saves them.

        Requests the Spotify user's top artists over a time range and
        stores them locally.

        Parameters
        ----------
        time_range : str
            The time range over which to collect the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.
        """

        limit = 50
        query_dict = {
            'limit': limit,
            'time_range': time_range
        }
        url = '/v1/me/top/artists'

        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
        self._top_artists[time_range] = results.json()['items']



    def _compile_top_genres(self, time_range):
        """Requests the user's top genres over a period and saves them.

        Requests the Spotify user's top genres over a time range and
        stores them locally.

        Parameters
        ----------
        time_range : str
            The time range over which to collect the top data. Can be
            one of 'short_term', 'medium_term', or 'long_term'.
        """

        top_artists = self.top_artists(time_range)

        # Top genres are just the genres of the top artists
        top_genres = [a['genres'] for a in top_artists]

        self._top_genres[time_range] = top_genres



    def _compile_personal_data(self):
        """Requests the Spotify user's personal data and saves it.

        Requests the Spotify user's personal data and stores it
        locally.
        """

        url = '/v1/me'
        results = spotify.make_authorized_request(self.session, url)

        self._personal_data = results.json()



    def _compile_audio_features(self):
        """Requests the user's extended music taste data and saves it.

        Requests the Spotify user's extended music taste data and
        stores it locally.
        """

        music_taste = self.music_taste() 

        ids = [t['id'] for t in music_taste]

        limit = 100
        
        # Split the song ids into sections (Spotify only lets you
        # request so many at a time)
        id_sections = split_into_subsections(ids, limit)
        for section in id_sections:
            url = '/v1/audio-features'
            query_dict = { 'ids': spotify.create_id_querystr(section) }
            results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

            tracks = results.json()['audio_features'] 

            music_taste = combine_track_json(music_taste, tracks)

        self._music_taste = music_taste



    def _compile_playlist_details(self):
        """Requests the user's extended playlist data and saves it.

        Requests the Spotify user's extended playlist data and
        stores it locally.
        """

        playlists = self.playlists()

        for p in playlists:
            url = '/v1/playlists/' + p['id']
            query_dict = { 'fields': 'followers' }
            results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)
            p['followers'] = results.json()['followers']

        self._playlists = playlists 
