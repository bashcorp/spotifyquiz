"""Miscellanous utility functions that help out with quiz creation."""

import random

def random_from_list(arr, num_choices, start=0, end=None):
    """Randomly picks a number of items from the bounds of the list.

    Randomly chooses a given number of items from the given list, or,
    if the start and end indices are specified, from that subset of the
    list. If there aren't enough elements in the list from which to
    pick the chosen number of items, will return None.

    Parameters
    ----------
    arr : list
        The list to pick items from
    num_choices : int
        How many items to pick from the given list
    start : int, optional
        The beginning index of the list subset to pick items from.
        (the default is 0, the beginning of the list)
    end : int, optional
        The ending index of the list subset to pick items from.
        (the default is None, which is treated as the end of the list)

    Returns
    -------
    list
        The list of the randomly chosen items, or None if the specified
        number of items could not be picked.
    """

    # if no end is specified, default to the end of the list
    if not end:
        end = len(arr)

    # If there are more choices than the length of the subset, fail
    if end-start < num_choices:
        return None

    # Pick indices
    indexes = random.sample(range(start, end), num_choices)

    # Compile items from indices
    return [arr[i] for i in indexes]



def random_from_list_blacklist(arr, blacklist, num_choices):
    """Picks a number of random items from the list, with a blacklist.

    Randomly chooses a given number of items from the given list. Will
    not pick any items that are in the specified blacklist. If there
    aren't enough elements in the list from which to pick the chosen
    number of items, will return None.

    Parameters
    ----------
    arr : list
        The list to pick items from
    blacklist : list
        A list of items which cannot be picked
    num_choices : int
        How many items to pick

    Returns
    -------
    list
        The list of the randomly chosen items, or None if the specified
        number of items could not be picked.
    """

    chosen = [] 

    # copy the list, so can delete items we've already tried to pick.
    # This way, we don't end up picking the same blacklisted items 
    # over and over
    items = arr.copy()

    for i in range(num_choices):
        # If list is empty, then we can't find enough items, sofail
        if not items:
            return None

        # Keep picking a random item from the list until it's valid.
        # Delete any picks that are invalid
        i = random.randint(0, len(items)-1)
        while len(items) > 1 and items[i] in blacklist:
            del items[i]
            i = random.randint(0, len(items)-1)

        # If the above loop chooses the very last item in the list, it
        # will not check if that item is blacklisted, so check here.
        # If it is blacklisted, then there aren't enough items to pick
        # from.
        if items[i] in blacklist:
            return None

        # Add the chosen items, and also delete it from the list so
        # it can't be picked again
        chosen.append(items[i])
        del items[i]

    return chosen



def split_into_subsections(arr, sublist_size):
    """Splits a list into several lists of the given size. 

    Splits a list into several lists of the given size. Depending on
    the length of the original list, the last list created may have
    fewer items than the specified sublist size.

    Parameters
    ----------
    arr : list
        The list to split into sub-lists.
    sublist_size : int
        The size to make each sublist, must be greater than 0>

    Returns
    -------
    list
        A list of all the sublists, or None if the sublist size is
        invalid.
    """

    # Lists of length < 1 don't make sense here.
    if sublist_size < 1:
        return None

    sublists = []

    # The start and end indices for the first sublist
    start = 0
    end = sublist_size

    while start < len(arr):
        # Set the end index, and limit it to the end of the list
        end = start+sublist_size
        if end > len(arr):
            end = len(arr)

        sublists.append(arr[start:end])
        start += sublist_size

    return sublists



def combine_track_json(tracks1, tracks2):
    """Combine two lists of track JSON objects, combining duplicates.

    Combines two lists of Spotify audio tracks (dicts in Spotify's
    track JSON format) into one list.

    A track is identified by its "id" field, and if a track with the
    same id appears in both lists, they will be merged. During merging,
    if each track has a value for the same field, the value from the
    track in the first list will be chosen.

    Parameters
    ----------
    tracks1 : list
        A list of Spotify audio track data, each formatted as Spotify's
        track JSON.
    tracks2 : list
        A second list of Spotify audio track data, each formatted as
        Spotify's track JSON.

    Returns
    -------
    list
        The two lists merged into one list of track dicts, each 
        formatted as Spotify's track JSON.
    """

    # Add each item in tracks2 to tracks1 
    for t2 in tracks2:
        found = False
        
        # Look for a track with the same ID in tracks1
        for i, t1 in enumerate(tracks1):
            if t1['id'] == t2['id']:
                # Merge the two track dicts into one
                # We want to keep dict values in t1 over the dict
                # values in t2, so have to do t2.update(t1). But we
                # want to return tracks1 as the final list, so update
                # the value in tracks1 with the updated version of t2.
                t2.update(t1)
                tracks1[i] = t2

                found = True
                break

        # If the track doesn't exist in tracks1, add it
        if not found:
            tracks1.append(t2)

    return tracks1



def call_rand_functions(functions, args, num):
    """Randomly calls a number of functions from the list, successfully

    Randomly picks functions from the given list and calls them until
    the given number of function calls have been successful. Each
    function will be called with the given argument list.

    Each function in the given list needs to return a non-None value
    on success and None on failure. If any of the functions is called
    and fails, it will not count towards the number of successful
    function calls.

    If this function is able to successfully call the proper number of
    functions, it will return a list of the return values of each of
    the successfully-called functions. If not, it will return None.

    Parameters
    ----------
    functions : list
        A list of functions from which to pick and call.
    args : list
        A list of arguments that will be passed to each function that
        is called.
    num : int
        The number of functions to successfully call.

    Returns
    -------
    list
        A list of the return values of each successful function call,
        or None if not enough of the functions could be successfully
        called.
    """

    # If there aren't enough functions, fail
    if len(functions) < num:
        return None

    results = []

    # Copy the list so that we can delete already called functions from
    # it
    copy = functions.copy()

    # Keep going until we've called enouogh functions successfully, or
    # there are no functions left in the list to pick from.
    while copy and len(results) < num:
        # Pick random function, call it
        i = random.randint(0, len(copy)-1)
        result = copy[i](*args)

        # If non-None value (success), add to results list
        if result is not None:
            results.append(result)

        # Remove from the list, so can't be picked again
        del copy[i]

    # If there weren't enough non-None return values, fail
    if len(results) != num:
        return None

    return results



def call_rand_functions_arg_sets(functions, args, num):
    """Randomly calls a number of functions from the list, successfully

    This is the same as call_rand_functions() above, except that
    instead of passing one argument list that is passed to each of
    the functions, the user passes a list of argument lists, one for
    each function in the function list. This removes the restriction
    of needing every function we're choosing from to have the same
    arguments.

    There must be an argument list for each function in the function
    list, otherwise this function will fail and return None.

    Parameters
    ----------
    functions : list
        A list of functions from which to pick and call.
    args : list
        A list of lists. Each list is an argument list that corresponds
        to one of the functions in the function list, and will be
        passed to that function if it is called.
    num : int
        The number of functions to successfully call.

    Returns
    -------
    list
        A list of the return values of each successful function call,
        or None if not enough of the functions could be successfully
        called.
    """

    # If there aren't enough functions, fail
    if len(functions) < num:
        return None

    # Must have an argument list for each function
    if len(args) != len(functions):
        return None

    results = []

    # Copy the lists so that we can delete already-called functions and
    # their argument lists
    func_copy = functions.copy()
    arg_copy = args.copy()

    # Keep going until we've called enough successful functions or
    # there aren't any functions left in the list
    while func_copy and arg_copy and len(results) < num:
        # Pick random function, call it
        i = random.randint(0, len(func_copy)-1)

        result = func_copy[i](*(arg_copy[i]))

        # If non-None value (success), add to results list
        if result is not None:
            results.append(result)

        # Remove from the list, so can't be picked again
        del func_copy[i]
        del arg_copy[i]

    # If there weren't enough non-None return values, fail
    if len(results) != num:
        return None

    return results



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

