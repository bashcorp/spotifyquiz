import random

def random_from_list(arr, num_choices, start=0, end=None):
    """
    Randomly chooses a given number (num_choices) of items from the given list.
    Picks from a subset of the list given by the start and end indices,
    which default to the entire list.
    """
    if not end: #If not specified, include the entire list
        end = len(arr)

    if end-start < num_choices:
        return None

    indexes = random.sample(range(start, end), num_choices)

    return [arr[i] for i in indexes]


def split_into_subsections(arr, sublist_size):
    """
    Split a list into several lists of a given size. If the length of the list is not
    evenly divisible by the size of the sublists, then the last list will have fewer items
    than sublist_size.
    """
    if sublist_size < 1:
        return None

    sublists = []
    start = 0
    end = sublist_size
    while start < len(arr):
        end = start+sublist_size
        if end > len(arr):
            end = len(arr)

        sublists.append(arr[start:end])
        start += sublist_size

    return sublists


def combine_track_json(tracks1, tracks2):
    """
    Takes two lists of track objects, in the Spotify JSON format, and combines them, putting
    tracks from tracks2 into tracks1. If each list has a track with the same ID, they will be
    merged, with precedence on the values in the tracks1 version of the track, over the tracks2
    version.
    """
    for t2 in tracks2:
        found = False
        for t1 in tracks1:
            if t1['id'] == t2['id']:
                non_destructive_update(t1, t2)
                found = True
                break

        if not found:
            tracks1.append(t2)


    return tracks1


def non_destructive_update(i1, i2):
    """
    Combines two dictionaries, putting the items from i2 into i1. It's similar to the built-in
    python method dictionary.update(), except that items in i1 have precedence over items in i2,
    meaning that if both dictionaries have the key, the value in i1 will be the one saved.
    """
    for k in i2.keys():
        if not i1.get(k):
            i1[k] = i2[k]

    return i1



def choose_items_not_in_list(item_list, excluded_items, num_chosen):
    """
    Chooses a number of items (num_chosen) from the given item_list, such that the chosen
    items are not in the list excluded_items.
    """
    chosen = [] 

    items = item_list.copy()
    for i in range(num_chosen):
        if not items:
            return None

        i = random.randint(0, len(items)-1)
        while len(items) > 1 and items[i] in excluded_items:
            del items[i]
            i = random.randint(0, len(items)-1)

        if items[i] in excluded_items:
            return None

        chosen.append(items[i])
        del items[i]

    return chosen
