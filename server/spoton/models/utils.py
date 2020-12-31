"""Miscellaneous models used by the Spotify quiz models."""

from django.db import models
from polymorphic.query import PolymorphicQuerySet


class PolyOwnerQuerySet(models.QuerySet):
    """Overrides Django QuerySet for a custom deletion method

    Overrides Django's QuerySet class so that deleting a QuerySet
    (a set of database objects) will delete each one individually.
    This is done so that an overridden delete() method in any model
    using this QuerySet will be called. Normally, deleting a QuerySet
    uses SQL commands and ignores the delete() methods.

    Django-Polymorphic has issues deleting sets of PolymorphicModel
    objects, and the fix to this is to override the delete() method of
    any model that contains a set (in a reverse Foreign Key
    relationship) of PolymorphicModel objects. When deleting sets
    of this model, you need to ensure that the overridden method
    is called, which is what this class does.

    For example, let's say ModelA is a PolymorphicModel, with a
    Foreign Key to ModelB, a normal Django model. So ModelB "has" many
    ModelA objects. Django-Polymorphic's issue is with deleting all of
    ModelB's ModelA objects. You need to override the ModelB delete()
    methods so that each ModelA object is deleted individually.
    What about deleting several ModelB objects at once? That won't call
    the overridden delete() method, so make the ModelB class use this
    class as its QuerySet, which will ensure that the overridden
    delete() method in ModelB is called any time a set of ModelB 
    objects is deleted.

    Any Model containing a reverse Foreign Key relationship to a
    PolymorphicModel should override its own delete() method and
    use this class (or the similar PolyOwnerPolymorphicQuerySet)
    as its QuerySet by putting
        objects = PolyOwnerQuerySet.as_manager()
    in its attributes.
    """

    def delete(self, *args, **kwargs):
        """
        Deletes each object in the QuerySet individually, so that the
        set's model's delete() method is called. See above for reasons.
        """
        for obj in self:
            obj.delete()

        super(PolyOwnerQuerySet, self).delete(*args, **kwargs)


class PolyOwnerPolymorphicQuerySet(PolymorphicQuerySet):
    """Overrides PolymorphicQuerySet for a custom deletion method

    Overrides Django-Polymorphic's PolymorphicQuerySet class so that
    deleting a QuerySet (a set of database objects) will delete each
    one individually. This is done so that an overridden delete()
    method in any model using this QuerySet will be called. Normally,
    deleting a QuerySet uses SQL commands and ignores the delete()
    methods.

    Any PolymorphicModel containing a reverse Foreign Key relationship
    to another PolymorphicModel should override its own delete() method
    and use this class as its QuerySet by putting
        objects = PolyOwnerQuerySet.as_manager()
    in its attributes.

    See the PolyOwnerQuerySet documentation for more details on why
    this is needed.
    """

    def delete(self, *args, **kwargs):
        """Deletes each object in the QuerySet individually.

        Deletes each object in the QuerySet individually, so that the
        set's model's delete() method is called. See above for reasons.
        """
        for obj in self:
            obj.delete()

        super(PolyOwnerPolymorphicQuerySet, self).delete(*args, **kwargs)





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

    return [Choice.create_album_choice(question, a, answer) for a in albums]


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

    return [Choice.create_artist_choice(question, a, answer) for a in artists]


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

    return [Choice.create_track_choice(question, t, answer) for t in tracks]


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

    return [Choice.create_genre_choice(question, g, answer) for g in genres]


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

    return [Choice.create_playlist_choice(question, p, answer) for p in playlists]


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
            answer = answer
    )
    
