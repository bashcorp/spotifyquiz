"""Creators functions used to create Spotify quiz models."""


from .quiz import Choice



def create_album_choices(question, albums, answer=False):
    """Creates choice objects from a list of JSON-formatted albums.

    Creates choice objects from a list of albums. Each album should be
    JSON, formatted the way the Spotify API does. The created objects
    will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns these choices.
    albums : list
        A list of albums, each being JSON in Spotify API format.
    answer : bool
        Whether the choices should be marked as correct or not.

    Returns
    -------
    list
        A list of the created quiz.Choice objects.
    """

    return [create_album_choice(question, a, answer) for a in albums]


def create_album_choice(question, album, answer=False):
    """Creates a choice object about a JSON-formatted album.

    Creates a choice object about an album. The choice's primary text is
    the album's name, and its secondary text is the artist's name.
    The album should be JSON, formatted the way the Spotify API does.
    The created object will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns this choice.
    album : dict 
        Album JSON data in the Spotify API format.
    answer : bool
        Whether the choice should be marked as correct or not.

    Returns
    -------
    list
        The newly created quiz.Choice object.
    """

    return Choice.objects.create(
        question = question,
        primary_text = album['name'],
        secondary_text = album['artists'][0]['name'],
        image_url = get_largest_image(album),
        answer = answer
    )


def create_artist_choices(question, artists, answer=False):
    """Creates choice objects from a list of JSON-formatted artists.

    Creates choice objects from a list of artists. Each artist should
    be JSON, formatted the way the Spotify API does. The created
    objects will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns these choices.
    artists : list
        A list of artists, each being JSON in Spotify API format.
    answer : bool
        Whether the choices should be marked as correct or not.

    Returns
    -------
    list
        A list of the created quiz.Choice objects.
    """

    return [create_artist_choice(question, a, answer) for a in artists]


def create_artist_choice(question, artist, answer=False):
    """Creates a choice object about a JSON-formatted artist.

    Creates a choice object about an artist. The choice's primary text
    is the artist's name, and its secondary text is empty. The album
    should be JSON, formatted the way the Spotify API does. The created
    object will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns this choice.
    artist : dict 
        Artist JSON data in the Spotify API format.
    answer : bool
        Whether the choice should be marked as correct or not.

    Returns
    -------
    list
        The newly created quiz.Choice object.
    """

    return Choice.objects.create(
        question = question,
        primary_text = artist['name'],
        image_url = get_largest_image(artist),
        answer = answer
    )


def create_track_choices(question, tracks, answer=False):
    """Creates choice objects from a list of JSON-formatted tracks.

    Creates choice objects from a list of tracks. Each track should be
    JSON, formatted the way the Spotify API does. The created objects
    will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns these choices.
    tracks : list
        A list of tracks, each being JSON in Spotify API format.
    answer : bool
        Whether the choices should be marked as correct or not.

    Returns
    -------
    list
        A list of the created quiz.Choice objects.
    """

    return [create_track_choice(question, t, answer) for t in tracks]


def create_track_choice(question, track, answer=False):
    """Creates a choice object about a JSON-formatted track.

    Creates a choice object about a track. The choice's primary text
    is the tracks's name, and its secondary text is the artist's name.
    The track should be JSON, formatted the way the Spotify API does.
    The created object will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns this choice.
    track : dict 
        Track JSON data in the Spotify API format.
    answer : bool
        Whether the choice should be marked as correct or not.

    Returns
    -------
    list
        The newly created quiz.Choice object.
    """

    return Choice.objects.create(
        question = question,
        primary_text = track['name'],
        secondary_text = track['artists'][0]['name'],
        answer = answer
    )


def create_genre_choices(question, genres, answer=False):
    """Creates choice objects from a list of genres.

    Creates choice objects from a list of genres. Each genre should
    be a string. The created objects will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns these choices.
    genres : list
        A list of genres, each being a str.
    answer : bool
        Whether the choices should be marked as correct or not.

    Returns
    -------
    list
        A list of the created quiz.Choice objects.
    """

    return [create_genre_choice(question, g, answer) for g in genres]


def create_genre_choice(question, genre, answer=False):
    """Creates a choice object about a genre.

    Creates a choice object about a genre. The choice's primary text is
    the genre, and its secondary text is empty. The created object
    will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns this choice.
    genre : str
        The genre
    answer : bool
        Whether the choice should be marked as correct or not.

    Returns
    -------
    list
        The newly created quiz.Choice object.
    """

    return Choice.objects.create(
            question = question,
            primary_text = genre,
            answer = answer
    )


def create_playlist_choices(question, playlists, answer=False):
    """Creates choice objects from a list of JSON-formatted playlists.

    Creates choice objects from a list of playlists. Each playlist
    should be JSON, formatted the way the Spotify API does. The created
    objects will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns these choices.
    playlists : list
        A list of playlists, each being JSON in Spotify API format.
    answer : bool
        Whether the choices should be marked as correct or not.

    Returns
    -------
    list
        A list of the created quiz.Choice objects.
    """

    return [create_playlist_choice(question, p, answer) for p in playlists]


def create_playlist_choice(question, playlist, answer=False):
    """Creates a choice object about a JSON-formatted playlist.

    Creates a choice object about a playlist. The choice's primary text
    is the playlists' name, and its secondary text is empty. The
    playlist should be JSON, formatted the way the Spotify API does.
    The created object will be committed to the database. 

    Parameters
    ----------
    question : quiz.Question
        The checkbox question model object that owns this choice.
    playlist : dict 
        Playlist JSON data in the Spotify API format.
    answer : bool
        Whether the choice should be marked as correct or not.

    Returns
    -------
    list
        The newly created quiz.Choice object.
    """

    return Choice.objects.create(
            question = question,
            primary_text = playlist['name'],
            image_url = get_largest_image(playlist),
            answer = answer
    )





def get_largest_image(data):
    """Returns the URL of the largest image in the given Spotify JSON.
    
    Using JSON returned from the Spotify API, finds the largest image
    (by height) specified the given dict and returns its URL. This can
    be passed a track object, and album object, any Spotify JSON dict
    that contains an 'images' field.

    Parameters
    ----------
    data : dict
        Spotify JSON to search in for images.

    Returns
    -------
    str
        The URL of the largest image found within the data, or None
        if there were no images listed.
    """
    
    if data.get('images') is None:
            return None

    url = None
    maxheight = 0
    
    for image in data.get('images'):
        if image.get('height') and image.get('height') > maxheight:
            maxheight = image.get('height')
            url = image.get('url')

    return url


