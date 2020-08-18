import random

def random_from_list(arr, num_choices, start=0, end=None):
    """
    Randomly chooses a given number (num_choices) of items from the given list.
    Picks from a subset of the list given by the start and end indices,
    which default to the entire list.
    """
    if not end: #If not specified, include the entire list
        end = len(arr)

    indexes = random.sample(range(start, end), num_choices)

    return [arr[i] for i in indexes]


def pick_and_call(quiz, user_data, funcs, num_of_calls, args=[]):
    func_indices = random.sample(range(0, len(funcs)), num_of_calls)
    for i in func_indices:
        funcs[i](quiz, user_data, args[random.randint(0, len(args))])
    

def split_into_subsections(arr, sublist_size):
    sublists = []
    start = 0
    end = sublist_size
    while start < len(arr):
        end = start+20
        if end > len(arr):
            end = len(arr)

        sublists.append(arr[start:end])
        start += 20

    return sublists


def combine_track_json(tracks1, tracks2):
    combination = []
    for t1 in tracks1:
        t = t1.copy()
        for t2 in tracks2:
            if t1['id'] == t2['id']:
                non_destructive_update(t1, t2)
                break

    return tracks1


def non_destructive_update(i1, i2):
    for k in i2.keys():
        if not i1.get(k):
            i1[k] = i2[k]


def create_id_querystr(ids):
    id_str = ""
    for id in ids:
        id_str += str(id) + ","
    id_str = id_str[:-1]
    return id_str

