from django.test import TransactionTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from spoton import spotify
from spoton.quiz.user_data import UserData
from spoton.tests.setup_tests import create_authorized_session

class UserDataExistsTests(TransactionTestCase):
    """
    Tests the get functions from the UserData class when the data already exists. All the
    functions have to do is return the data.
    """

    def test_fields_initiated(self):
        u = UserData(None)
        self.assertIsNone(u._music_taste)
        self.assertIsNone(u._playlists)
        self.assertIsNone(u._recently_played)
        self.assertIsNone(u._saved_tracks)
        self.assertIsNone(u._saved_albums)
        self.assertIsNone(u._followed_artists)
        self.assertIsNone(u._personal_data)

        self.assertEqual(u._top_artists, {})
        self.assertEqual(u._top_tracks, {})
        self.assertEqual(u._top_genres, {})

    
    def test_get_personal_data_exists(self):
        """
        If _personal_data is not None, personal_data() should return it.
        """
        u = UserData(None)
        test_data = { 'test': 'hello' }
        u._personal_data = test_data
        self.assertEqual(u.personal_data(), test_data)


    def test_get_music_taste_exists(self):
        """
        If _music_taste is not None, music_taste() should return it.
        """
        u = UserData(None)
        test_data = ['test', 'hello']
        u._music_taste = test_data
        self.assertEqual(u.music_taste(), test_data)


    def test_get_music_taste_with_audio_features_exists(self):
        """
        If _music_taste is data with audio features in it, personal_data() should return it.
        """
        u = UserData(None)
        test_data = [{'id': 5, 'energy': 0}, {'id': 2, 'energy': 5}]
        u._music_taste = test_data
        self.assertEqual(u.music_taste_with_audio_features(), test_data)

    
    def test_get_playlists_exists(self):
        """
        If _playlists is not None, playlists() should return it.
        """
        u = UserData(None)
        test_data = ['test', 'hello']
        u._playlists = test_data
        self.assertEqual(u.playlists(), test_data)


    def test_get_playlists_detailed_exists(self):
        """
        If _playlists has detailed playlist data, playlists() should return it.
        """
        u = UserData(None)
        test_data = [{'followers': 0}, {'followers': 5}]
        u._playlists = test_data
        self.assertEqual(u.playlists_detailed(), test_data)


    def test_get_recently_played_exists(self):
        """
        If _recently_played is not None, recently_played() should return it.
        """
        u = UserData(None)
        test_data = ['test', 'hello']
        u._recently_played = test_data
        self.assertEqual(u.recently_played(), test_data)

    
    def test_get_top_artists_longterm_exists(self):
        """
        If _top_artists['long_term'] is not None, top_artists('long_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_artists['long_term'] = test_data
        self.assertEqual(u.top_artists('long_term'), test_data)


    def test_get_top_artists_mediumterm_exists(self):
        """
        If _top_artists['medium_term'] is not None, top_artists('medium_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_artists['medium_term'] = test_data
        self.assertEqual(u.top_artists('medium_term'), test_data)


    def test_get_top_artists_shortterm_exists(self):
        """
        If _top_artists['short_term'] is not None, top_artists('short_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_artists['short_term'] = test_data
        self.assertEqual(u.top_artists('short_term'), test_data)


    def test_get_top_tracks_longterm_exists(self):
        """
        If _top_tracks['long_term'] is not None, top_tracks('long_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_tracks['long_term'] = test_data
        self.assertEqual(u.top_tracks('long_term'), test_data)


    def test_get_top_tracks_mediumterm_exists(self):
        """
        If _top_tracks['medium_term'] is not None, top_tracks('medium_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_tracks['medium_term'] = test_data
        self.assertEqual(u.top_tracks('medium_term'), test_data)


    def test_get_top_tracks_shortterm_exists(self):
        """
        If _top_tracks['short_term'] is not None, top_tracks('short_term') should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._top_tracks['short_term'] = test_data
        self.assertEqual(u.top_tracks('short_term'), test_data)


    def test_get_top_genres_longterm_exists(self):
        """
        If _top_genres['long_term'] is not None, top_genres('long_term') should return it.
        """
        u = UserData(None)
        test_data = [['hello', 'there'], ['goodbye', 'now']]
        u._top_genres['long_term'] = test_data
        self.assertEqual(u.top_genres('long_term'), test_data)


    def test_get_top_genres_mediumterm_exists(self):
        """
        If _top_genres['medium_term'] is not None, top_genres('medium_term') should return it.
        """
        u = UserData(None)
        test_data = [['hello', 'there'], ['goodbye', 'now']]
        u._top_genres['medium_term'] = test_data
        self.assertEqual(u.top_genres('medium_term'), test_data)


    def test_get_top_genres_shortterm_exists(self):
        """
        If _top_genres['short_term'] is not None, top_genres('short_term') should return it.
        """
        u = UserData(None)
        test_data = [['hello', 'there'], ['goodbye', 'now']]
        u._top_genres['short_term'] = test_data
        self.assertEqual(u.top_genres('short_term'), test_data)


    def test_get_saved_tracks_exists(self): 
        """
        If _saved_tracks is not None, saved_tracks() should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._saved_tracks = test_data
        self.assertEqual(u.saved_tracks(), test_data)


    def test_get_saved_albums_exists(self): 
        """
        If _saved_albums is not None, saved_albums() should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._saved_albums = test_data
        self.assertEqual(u.saved_albums(), test_data)


    def test_get_followed_artists_exists(self):
        """
        If _followed_artists is not None, followed_artists() should return it.
        """
        u = UserData(None)
        test_data = ['hello', 'goodbye']
        u._followed_artists = test_data
        self.assertEqual(u.followed_artists(), test_data)


    def test_get_playlist_with_tracks_exists(self):
        """
        If the playlist with the given ID exists in _playlists and it already has a list of
        tracks, return that playlist data.
        """
        u = UserData(None)
        test_data = [{'id': '0', 'tracks': {'items': []}}]
        u._playlists = test_data
        self.assertEqual(u.get_playlist_with_tracks('0'), test_data[0])


     
class UserDataCompilationTests(StaticLiveServerTestCase):
    """
    Tests the methods that request and compile data using the Spotify API. This is achieved
    by calling the get methods when there is no data in the corresponding variables. Those
    methods will trigger these compilation functions.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(UserDataCompilationTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)
        #cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        #cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        #cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(UserDataCompilationTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_compile_music_taste(self):
        """
        _compile_music_taste() should request compile data about the user's music taste from
        Spotify and store it in the _music_taste variable.
        """
        u = UserData(self.session)
        data = u.music_taste()
        self.assertGreaterEqual(len(data), 50)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_playlists(self):
        """
        compile_playlists() should request compile data about the user's playlists from Spotify
        and store it in the _playlists variable.
        """
        u = UserData(self.session)
        data = u.playlists()
        self.assertGreaterEqual(len(data), 5)
        for p in data:
            self.assertEqual(p['type'], 'playlist')

    
    def test_compile_saved_tracks(self):
        """
        compile_saved_tracks() should request data about the user's saved tracks from Spotify
        and store it in the _saved_tracks variable.
        """
        u = UserData(self.session)
        data = u.saved_tracks()
        self.assertGreaterEqual(len(data), 5)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_saved_albums(self):
        """
        compile_saved_albums() should request data about the user's saved albums from Spotify
        and store it in the _saved_albums variable.
        """
        u = UserData(self.session)
        data = u.saved_albums()
        self.assertGreaterEqual(len(data), 5)
        for a in data:
            self.assertEqual(a['type'], 'album')


    def test_compile_followed_artists(self):
        """
        compile_followed_artists() should request data about the user's saved albums from
        Spotify and store it in the _saved_albums variable.
        """
        u = UserData(self.session)
        data = u.followed_artists()
        self.assertGreaterEqual(len(data), 2)
        for a in data:
            self.assertEqual(a['type'], 'artist')

    
    def test_compile_recently_played(self):
        """
        compile_followed_artists() should request data about the user's saved albums from
        Spotify and store it in the _saved_albums variable.
        """
        u = UserData(self.session)
        data = u.recently_played()
        self.assertEqual(len(data), 50)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_top_tracks_longterm(self):
        """
        compile_top_tracks('long_term') should request data about the user's top tracks from
        Spotify and store it in the _top_tracks['long_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_tracks('long_term')
        self.assertEqual(len(data), 50)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_top_tracks_mediumterm(self):
        """
        compile_top_tracks('medium_term') should request data about the user's top tracks from
        Spotify and store it in the _top_tracks['medium_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_tracks('medium_term')
        self.assertEqual(len(data), 50)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_top_tracks_shortterm(self):
        """
        compile_top_tracks('short_term') should request data about the user's top tracks from
        Spotify and store it in the _top_tracks['short_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_tracks('short_term')
        self.assertGreaterEqual(len(data), 10)
        for t in data:
            self.assertEqual(t['type'], 'track')


    def test_compile_top_artists_longterm(self):
        """
        compile_top_artists('long_term') should request data about the user's top artists from
        Spotify and store it in the _top_artists['long_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_artists('long_term')
        self.assertEqual(len(data), 50)
        for a in data:
            self.assertEqual(a['type'], 'artist')


    def test_compile_top_artists_mediumterm(self):
        """
        compile_top_tracks('medium_term') should request data about the user's top tracks from
        Spotify and store it in the _top_tracks['medium_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_artists('medium_term')
        self.assertEqual(len(data), 50)
        for a in data:
            self.assertEqual(a['type'], 'artist')


    def test_compile_top_artists_shortterm(self):
        """
        compile_top_tracks('short_term') should request data about the user's top tracks from
        Spotify and store it in the _top_tracks['short_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_artists('short_term')
        self.assertGreaterEqual(len(data), 10)
        for a in data:
            self.assertEqual(a['type'], 'artist')


    def test_compile_top_genres_longterm(self):
        """
        compile_top_genres('long_term') should request data about the user's top genres from
        Spotify and store it in the _top_genres['long_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_genres('long_term')
        self.assertGreaterEqual(len(data), 50)
        for gl in data:
            self.assertIsInstance(gl, list)
            for g in gl:
                self.assertIsInstance(g, str)


    def test_compile_top_genres_mediumterm(self):
        """
        compile_top_genres('medium_term') should request data about the user's top genres from
        Spotify and store it in the _top_genres['medium_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_genres('medium_term')
        self.assertGreaterEqual(len(data), 50)
        for gl in data:
            self.assertIsInstance(gl, list)
            for g in gl:
                self.assertIsInstance(g, str)


    def test_compile_top_genres_shortterm(self):
        """
        compile_top_genres('short_term') should request data about the user's top genres from
        Spotify and store it in the _top_genres['short_term'] variable.
        """
        u = UserData(self.session)
        data = u.top_genres('short_term')
        self.assertGreaterEqual(len(data), 10)
        for gl in data:
            self.assertIsInstance(gl, list)
            for g in gl:
                self.assertIsInstance(g, str)


    def test_compile_personal_data(self):
        """
        compile_personal_data() should request data about the user's personal data from
        Spotify and store it in the _personal_data variable.
        """
        u = UserData(self.session)
        data = u.personal_data()
        self.assertIsNotNone(data.get('followers'))
        self.assertIsNotNone(data.get('display_name'))

    
    def test_compile_audio_features(self):
        """
        compile_audio_features() should request data about audio features of the user's
        music taste from Spotify and store it in the _personal_data variable.
        """
        u = UserData(self.session)
        data = u.music_taste_with_audio_features()
        self.assertGreaterEqual(len(data), 50)
        for t in data:
            self.assertEquals(t['type'], 'track')
            self.assertIsNotNone(t.get('energy'))
            self.assertIsNotNone(t.get('danceability'))
            self.assertIsNotNone(t.get('valence'))

    
    def test_compile_playlist_details(self):
        """
        compile_playlist_details() should request detailed data 
        """
        u = UserData(self.session)
        data = u.playlists_detailed()
        self.assertGreaterEqual(len(data), 5)
        for p in data:
            self.assertEquals(p['type'], 'playlist')
            self.assertIsNotNone(p.get('followers'))


    def test_get_playlist_with_tracks(self):
        u = UserData(self.session)
        playlists = u.playlists()

        data = u.get_playlist_with_tracks(playlists[0]['id'])

        self.assertEquals(data['type'], 'playlist')
        self.assertIsNotNone(data['tracks']['items'])



class UserDataErrorTests(StaticLiveServerTestCase):
    """
    Tests that certain cases of improper data cause the proper errors in the UserData class.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(UserDataErrorTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(UserDataErrorTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_bad_session_errors(self):
        """
        Any get function for user data should raise an exception if the session variable
        is not a valid Spotify-authorized Django session.
        """
        u = UserData(None)

        self.assertRaises(Exception, u.personal_data)
        self.assertRaises(Exception, u.music_taste)
        self.assertRaises(Exception, u.music_taste_with_audio_features)
        self.assertRaises(Exception, u.playlists)
        self.assertRaises(Exception, u.playlists_detailed)
        self.assertRaises(Exception, u.recently_played)
        self.assertRaises(Exception, u.top_artists, 'long_term')
        self.assertRaises(Exception, u.top_tracks, 'long_term')
        self.assertRaises(Exception, u.top_genres, 'long_term')
        self.assertRaises(Exception, u.saved_tracks)
        self.assertRaises(Exception, u.saved_albums)
        self.assertRaises(Exception, u.followed_artists)
        self.assertRaises(Exception, u.get_playlist_with_tracks)


    def test_bad_time_range(self):
        """
        top_artists, top_tracks, top_genres are dictionaries where the keys are the three
        different time ranges that Spotify uses: long_term, medium_term, short_term. This
        ensures that the get functions raise an exception if the dictionary key is not 
        one of these three ranges.
        """
        u = UserData(self.session)

        self.assertRaises(spotify.SpotifyRequestException, u.top_artists, 'asdf')
        self.assertRaises(spotify.SpotifyRequestException, u.top_tracks, 'asdf')
        self.assertRaises(spotify.SpotifyRequestException, u.top_genres, 'asdf')
