"""Tests the utility functions from the quiz module.

Tests the file spoton/quiz/utils.py.
"""

from django.test import TransactionTestCase, TestCase

from spoton.quiz.utils import *


class RandomFromListTests(TestCase):
    """
    Tests random_from_list(), which should randomly choose a certain
    number of items from the given list, within the bounds provided in
    the arguments.
    """

    def test_random_from_list_no_bounds(self):
        """
        random_from_list() should choose a certain number of items from
        the entire list, if no bounds are provided.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4)

        for i in chosen:
            self.assertIn(i, arr)

        no_dupes = list(set(chosen))
        self.assertEqual(len(no_dupes), len(chosen))


    def test_random_from_list_bounds(self):
        """
        random_from_list() should choose a certain number of items from
        a given list, within the bounds provided in the arguments.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4, start=1, end=6)

        self.assertNotIn(1, chosen)
        self.assertNotIn(7, chosen)

        for i in chosen:
            self.assertIn(i, arr)

        no_dupes = list(set(chosen))
        self.assertEqual(len(no_dupes), len(chosen))


    def test_random_from_list_bounds_no_end(self):
        """
        random_from_list() should choose a certain number of items from
        a given list, within the bounds provided in the arguments. If
        no end bound is provided, it should pick until the end of the
        list.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4, start=3)

        self.assertNotIn(1, chosen)
        self.assertNotIn(2, chosen)
        self.assertNotIn(3, chosen)

        for i in chosen:
            self.assertIn(i, arr)

        no_dupes = list(set(chosen))
        self.assertEqual(len(no_dupes), len(chosen))


    def test_random_from_list_too_many_choices(self):
        """
        If the number of choices passed to random_from_list() exceeds
        the size of the list, it should return None.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4, start=4, end=6)

        self.assertIsNone(chosen)



class SplitIntoSubsectionsTests(TestCase):
    """
    Tests split_into_subsections(), which should split a given list
    into several smaller lists of the same specified size. The last
    list could have fewer items than specified.
    """

    def test_split_into_subsections(self):
        """
        split_into_subsections() should split a given list into several
        smaller lists of the same specified size. The last list could
        have fewer items than specified.
        """
        arr = range(100)

        results = split_into_subsections(arr, 10)

        sublists = [
            range(0, 10),
            range(10, 20),
            range(20, 30),
            range(30, 40),
            range(40, 50),
            range(50, 60),
            range(60, 70),
            range(70, 80),
            range(80, 90),
            range(90, 100)
        ]
        
        self.assertCountEqual(results, sublists)


    def test_split_into_subsections_smaller_end(self):
        """
        split_into_subsections() should split a given list into several
        smaller lists of the same given size. The last list could have
        fewer items than specified.
        """
        arr = range(25)

        results = split_into_subsections(arr, 10)

        sublists = [
            range(0, 10),
            range(10, 20),
            range(20, 25)
        ]

        self.assertCountEqual(results, sublists)


    def test_split_into_subsections_bad_sublist_size(self):
        """
        If the subsection size is less than 1, split_into_subsections()
        should return None.
        """
        arr = range(10)
        results = split_into_subsections(arr, 0)
        self.assertIsNone(results)

        

class CombineTrackJsonTests(TestCase):
    """
    Tests combine_track_json(), which should combine two lists of track
    JSON into one, merging any duplicate tracks.
    """

    def test_combine_track_json(self):
        """
        combine_track_json() should combine two lists of tracks into
        one, merging any duplicate tracks. If the track appears in both
        lists, they should be merged with preference to the fields in
        the first list of tracks.
        """
        tracks1 = [
            {'id': 1, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 2, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 3, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 4, 'attr1': 'val1', 'attr2': 'val2'},
        ]
        tracks2 = [
            {'id': 5, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 6, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 3, 'attr1': 'val2', 'attr2': 'val3'},
            {'id': 4, 'attr1': 'val8', 'attr3': 'val3'},
        ]
        
        combined = [
            {'id': 1, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 2, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 3, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 4, 'attr1': 'val1', 'attr2': 'val2', 'attr3': 'val3'},
            {'id': 5, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 6, 'attr1': 'val1', 'attr2': 'val2'},
        ]

        results = combine_track_json(tracks1, tracks2)
        self.assertCountEqual(results, combined)
        self.assertCountEqual(tracks1, combined)


    def test_combine_track_json_emtpy_track1(self):
        """
        combine_track_json() should combine two lists of tracks into 1,
        merging any duplicate tracks.
        """
        tracks2 = [
            {'id': 1, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 2, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 3, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 4, 'attr1': 'val1', 'attr2': 'val2'},
        ]

        t2_orig = tracks2.copy()

        results = combine_track_json([], tracks2)
        self.assertCountEqual(results, t2_orig)
        self.assertCountEqual(tracks2, t2_orig)


    def test_combine_track_json_empty_track2(self):
        """
        combine_track_json() should combine two lists of tracks into 1, 
        merging any duplicate tracks.
        """
        tracks1 = [
            {'id': 1, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 2, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 3, 'attr1': 'val1', 'attr2': 'val2'},
            {'id': 4, 'attr1': 'val1', 'attr2': 'val2'},
        ]

        t1_orig = tracks1.copy()

        results = combine_track_json(tracks1, [])
        self.assertCountEqual(results, t1_orig)
        self.assertCountEqual(tracks1, t1_orig)

    

class ChooseItemsNotInListTests(TestCase):
    """
    Tests random_from_list_blacklist(), which chooses a given number of
    items from the given list, with the condition that the chosen items
    are not in a given blacklist.
    """

    def test_random_from_list_blacklist(self):
        """
        random_from_list_blacklist() should choose a given number of
        items from a given list, such that the items are not in a given
        exclusion list.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = random_from_list_blacklist(item_list, excluded_items, 3)

        for i in results:
            self.assertIn(i, item_list)
            self.assertNotIn(i, excluded_items)

        non_dupes = list(set(results))
        self.assertEquals(len(non_dupes), len(results))


    def test_random_from_list_blacklist_just_enough(self):
        """
        random_from_list_blacklist() should choose a given number of
        items from a given list, such that the items are not in a given
        exclusion list.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = random_from_list_blacklist(item_list, excluded_items, 5)

        for i in results:
            self.assertIn(i, item_list)
            self.assertNotIn(i, excluded_items)

        non_dupes = list(set(results))
        self.assertEquals(len(non_dupes), len(results))


    def test_random_from_list_blacklist_not_enough_items(self):
        """
        If there are not enough whitelisted items to pick from,
        random_from_list_blacklist() should return None.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = random_from_list_blacklist(item_list, excluded_items, 6)

        self.assertIsNone(results)


def func0(i):
    return i

def func1(i):
    return i+1

def func2(i):
    return i+2

def func3(i):
    return i+3

def func4():
    return 1

def func5():
    return 2

def func6(i):
    return None


class CallRandFunctionsTests(TestCase):
    """
    Tests call_rand_functions(), which should accept a list of
    functions, an argument list, and the number of functions to call.
    It should randomly call these functions until it's successfully
    called the specified number of functions. Each function called
    should be passed the given arugment list. A successful function
    call returns not-None. If the specified number of functions were
    called successfully, the function returns a list of the functions'
    return values. If not, the function returns None.
    """

    def test_call_rand_functions(self):
        """
        call_rand_functions() should successfully call a specified
        number of functions from a given list of functions, and return
        a list of their return values.
        """
        functions = [func0, func1, func2, func3]
        args = [3]

        results = call_rand_functions(functions, args, 3)

        self.assertIsNotNone(results)

        poss_results = list(range(3, 3+4))
        for i in results:
            self.assertIn(i, poss_results)

        unique = list(set(results))
        self.assertEqual(len(results), len(unique))
    

    def test_call_rand_functions_no_args(self):
        """
        call_rand_functions() should also work if there are no
        arguments in the arg list.
        """
        functions = [func4, func5]
        args = []

        results = call_rand_functions(functions, args, 2)

        self.assertCountEqual(results, [1, 2])


    def test_call_rand_functions_zero_return(self):
        """
        call_rand_functions() should not treat a function returning 0
        as a fail (i.e. should not interpret 0 as None)
        """
        functions = [func0, func0]
        args = [0]

        results = call_rand_functions(functions, args, 1)

        self.assertCountEqual(results, [0])


    def test_call_rand_functions_not_enough_funcs(self):
        """
        call_rand_functions() should return None if there aren't enough
        functions to call the given number.
        """
        functions = [func0, func1, func2, func3]
        args = [3]

        results = call_rand_functions(functions, args, 5)

        self.assertIsNone(results)


    def test_call_rand_functions_funcs_return_none(self):
        """
        call_rand_functions() should return None if there are enough
        functions to call the given number, but too many of them return
        None.
        """
        functions = [func0, func1, func2, func6, func6]
        args = [5]

        results = call_rand_functions(functions, args, 4)

        self.assertIsNone(results)



class CallRandFunctionsArgSetsTests(TestCase):
    """
    Tests call_rand_functions_arg_sets(), which is the same as
    call_rand_functions(), except that instead of one argument list
    for all the functions, the function is passed a list of argument
    list, each one corresponding to one of the functions in the
    function list. When a function from the list is called, it gets
    passed its own argument list.
    """

    def test_call_rand_functions_arg_sets(self):
        """
        call_rand_functions_arg_sets() should successfully call a
        specified number of functions from a given list of functions,
        and return a list of their return values.
        """
        functions = [func0, func0, func0, func0]
        args = [[3], [4], [5], [6]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertIsNotNone(results)

        poss_results = list(range(3, 7))
        for i in results:
            self.assertIn(i, poss_results)

        unique = list(set(results))
        self.assertEqual(len(unique), len(results))


    def test_call_rand_functions_arg_sets_just_enough(self):
        """
        call_rand_functions_arg_sets() should successfully call a
        specified number of functions from a given list of functions,
        and return a list of their return values.
        """
        functions = [func0, func0, func0]
        args = [[1], [2], [3]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertCountEqual(results, [1, 2, 3])


    def test_call_rand_functions_arg_sets_zero_return(self):
        """
        call_rand_functions_arg_sets() should not treat a function
        returning 0 as a fail (i.e. should not interpret 0 as None)
        """
        functions = [func0, func0]
        args = [[0], [0]]

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertCountEqual(results, [0, 0])


    def test_call_rand_functions_arg_sets_no_args(self):
        """
        call_rand_functions_arg_sets() should also work if there are no
        argument lists in the parameter.
        """
        functions = [func4, func5]
        args = []

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_not_enough_funcs(self):
        """
        call_rand_functions_arg_sets() should return None if there
        aren't enough functions to call the given number.
        """
        functions = [func0, func1, func2, func3]
        args = [[3], [4], [5], [6]]

        results = call_rand_functions_arg_sets(functions, args, 5)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_not_enough_arguments(self):
        """
        call_rand_functions() should return None if there are a
        different number of argument lists given than the number of
        functions
        """
        functions = [func0, func1, func2, func3]
        args = [[3], [4], [5]]

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_funcs_return_none(self):
        """
        call_rand_functions() should return None if there are enough
        functions to call the given number, but too many of them return
        None.
        """
        functions = [func0, func1, func2, func6, func6]
        args = [[3], [4], [5], [6], [7]]

        results = call_rand_functions_arg_sets(functions, args, 4)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_ensure_pairings(self):
        """
        call_rand_functions() should match functions and argument lists
        by index: the 2nd function in the list should be called with
        the 2nd argument list in that list.
        """
        functions = [func0, func1, func2, func3]
        args = [[4], [3], [2], [1]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertCountEqual(results, [4, 4, 4])




class GetLargestImageTests(TestCase):
    """
    get_largest_image() should return the largest image specified in
    the 'images' field of a Spotify-returned JSON dict. Tests the
    function with possible inputs.
    """

    def test_get_largest_image(self):
        """
        get_largest_image() should return the largest image specified
        in the 'images' field.
        """
        data = { 'images' : [
            { 'height': 200, 'width': 200, 'url': '200url' },
            { 'height': 640, 'width': 640, 'url': '640url' },
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)

        self.assertEqual(url, '640url')


    def test_get_largest_image_one_option(self):
        """
        get_largest_image() should return the image specified
        in the 'images' field, if there is only one.
        """
        data = { 'images' : [
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)
        
        self.assertEqual(url, '300url')


    def test_get_largest_image_no_options(self):
        """
        get_largest_image() should return None if the 'images' field is
        an empty array.
        """
        data = { 'images' : [] }

        url = get_largest_image(data)

        self.assertIsNone(url)

    
    def test_get_largest_image_no_field(self):
        """
        get_largest_image() should return None if the 'images' field
        does not exist.
        """
        data = { 'test': 'hi' }

        url = get_largest_image(data)

        self.assertIsNone(url)


    def test_get_largest_image_bad_size_format(self):
        """
        get_largest_image() should return None if the images do not
        specify their size.
        """
        data = { 'images': [
            { 'size': 200, 'url': '200url' },
            { 'size': 300, 'url': '300url' },
            { 'size': 640, 'url': '640url' },
            ]}

        url = get_largest_image(data)
        
        self.assertIsNone(url)

    
    def test_get_largest_image_no_url_field(self):
        """
        get_largest_image() should return None if the images do not
        specify a url.
        """
        data = { 'images': [
            { 'height': 200 },
            { 'height': 300 },
            { 'height': 640 },
            ]}

        url = get_largest_image(data)

        self.assertIsNone(url)


