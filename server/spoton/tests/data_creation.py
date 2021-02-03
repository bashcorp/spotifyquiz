"""Utility data-creation functions for testing this server.

Utility functions that create Spotify JSON data more easily than
creating it by hand.
"""


def create_tracks(num, id=0):
    """
    Creates and returns an array with the specified number of track
    dicts, with increasing ids starting at the given id.
    """
    tracks = []
    
    for i in range(num):
        tracks.append({'id': id+i, 'artists':[]})

    return tracks



def create_albums(num, id=0):
    """
    Creates and returns an array with the specified number of album
    dicts, with increasing ids starting at the given id.
    """
    albums = []

    for i in range(num):
        albums.append({'id': id+i, 'artists':[], 'images':[]})

    return albums



def create_artists(num, id=0):
    """
    Creates and returns an array with the specified number of artist
    dicts, with increasing ids starting at the given id.
    """
    artists = []
    for i in range(num):
        artists.append({'id': id+i, 'images':[]})

    return artists



def create_playlists(num, id=0):
    """
    Creates and returns an array with the specified number of playlist
    dicts, with increasing ids starting at the given id.
    """
    playlists = []
    for i in range(num):
        playlists.append({'id': id+i, 'tracks':{'total':0, 'items':[]},
            'images':[]})
    return playlists



def create_image(width=200, height=200, url='200url'):
    """
    Creates and returns an image dict with the given width, height,
    and url.
    """

    return {'width': width, 'height': height, 'url': url}



def create_followers(followers):
    """
    Creates and returns a followers dict with the given number of
    followers.
    """
    return {'total': followers}



def json_add_field(json, field, value, arr=False):
    """
    Adds the given field to each of the dicts in the given array, with
    the given value. If arr is False, value is assigned to each of 
    the fields. If arr is True, value is treated as an array, and each
    field is assigned the next element within the array.
    """

    for i,t in enumerate(json):
        if arr:
            t[field] = value[i]
        else:
            t[field] = value


def json_add_to_field(json, field, value, arr=False):
    """
    For each dict entry in the given array, adds an entry to the array
    stored in the dict's 'field' field. If arr is False, each dict's
    entry is 'value'. If arr is True, 'value' is treated as an array,
    and each entry is the next element in that array.
    """
    for i,t in enumerate(json):
        if arr:
            t[field].append(value[i])
        else:
            t[field].append(value)


def json_add_name(json, value, index=0):
    """
    Adds a name field to the given array of JSON dicts. 'value' is
    the name template. Each name is the template with a number
    appended to it, incrementing from the value of 'index'.
    """

    for i,t in enumerate(json):
        t['name'] = value + str(index+i)


def playlist_add_track(playlist, tracks):
    """
    Adds a list of tracks to the given playlist, and updates the total
    number of tracks saved in that playlist.
    """
    for t in tracks:
        playlist['tracks']['items'].append({'track': t})
    playlist['tracks']['total'] += len(tracks)


