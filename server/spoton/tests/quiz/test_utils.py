from django.test import TransactionTestCase, TestCase

from spoton.quiz.utils import *


class RandomFromListTests(TestCase):
    """
    random_from_list() should choose a certain number of items from a given list, within the
    bounds provided in the arguments.
    """

    def test_random_from_list_no_bounds(self):
        """
        random_from_list() should choose a certain number of items from a given list, within the
        bounds provided in the arguments.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4)

        for i in chosen:
            self.assertIn(i, arr)

        no_dupes = list(set(chosen))
        self.assertEqual(len(no_dupes), len(chosen))


    def test_random_from_list_bounds(self):
        """
        random_from_list() should choose a certain number of items from a given list, within the
        bounds provided in the arguments.
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
        random_from_list() should choose a certain number of items from a given list, within the
        bounds provided in the arguments. If no end bound is provided, it should be the length of
        the list.
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
        If the number of choices passed to random_from_list() exceeds the size of the list,
        it should return None.
        """
        arr = [1, 2, 3, 4, 5, 6, 7]
        chosen = random_from_list(arr, 4, start=4, end=6)

        self.assertIsNone(chosen)



class SplitIntoSubsectionsTests(TestCase):
    """
    split_into_subsections() should split a given list into several smaller lists of the same
    given size. The last list could have fewer items than specified.
    """

    def test_split_into_subsections(self):
        """
        split_into_subsections() should split a given list into several smaller lists of the same
        given size. The last list could have fewer items than specified.
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
        split_into_subsections() should split a given list into several smaller lists of the same
        given size. The last list could have fewer items than specified.
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
        If the subsection size is less than 1, split_into_subsections() should return None.
        """
        arr = range(10)
        results = split_into_subsections(arr, 0)
        self.assertIsNone(results)

        

class CombineTrackJsonTests(TestCase):
    """
    combine_track_json() should combine two lists of tracks into 1, combining values in
    any duplicate tracks.
    """

    def test_combine_track_json(self):
        """
        combine_track_json() should combine two lists of tracks into 1, combining values in
        any duplicate tracks.
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
        combine_track_json() should combine two lists of tracks into 1, combining values in
        any duplicate tracks.
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
        combine_track_json() should combine two lists of tracks into 1, combining values in
        any duplicate tracks.
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

    


class NonDestructiveUpdateTests(TestCase):
    """
    non_destructive_update() merges two dictionaries (i1 and i2) into i1. If the dicts have
    the same key, the value of i1 will be the one preserved.
    """

    def test_non_destructive_update(self):
        """
        non_destructive_update() merges two dictionaries (i1 and i2) into i1. If the dicts have
        the same key, the value of i1 will be the one preserved.
        """
        i1 = {'id': 4, 'attr1': 'testing', 'attr2': 'test2'}
        i2 = {'id': 5, 'attr3': 'hello', 'attr2': 'test4'}

        combined = {'id': 4, 'attr1': 'testing', 'attr2': 'test2', 'attr3': 'hello'}
        results = non_destructive_update(i1, i2)

        self.assertEquals(results, combined)
        self.assertEquals(i1, combined)


    def test_non_destructive_update_no_i1(self):
        """
        non_destructive_update() merges two dictionaries (i1 and i2) into i1. If the dicts have
        the same key, the value of i1 will be the one preserved.
        """
        i2 = {'id': 4, 'attr1': 'testing', 'attr2': 'test2'}
        i2_orig = i2.copy()

        results = non_destructive_update({}, i2)

        self.assertEquals(results, i2_orig)
        self.assertEquals(i2, i2_orig)


    def test_non_destructive_update_no_i2(self):
        """
        non_destructive_update() merges two dictionaries (i1 and i2) into i1. If the dicts have
        the same key, the value of i1 will be the one preserved.
        """
        i1 = {'id': 4, 'attr1': 'testing', 'attr2': 'test2'}
        i1_orig = i1.copy()

        results = non_destructive_update(i1, {})

        self.assertEquals(results, i1_orig)
        self.assertEquals(i1, i1_orig)


class ChooseItemsNotInListTests(TestCase):
    """
    Tests choose_items_not_in_list(), which chooses a given number of items from the given list,
    with the condition that the chosen items are not in a given exclusion list.
    """

    def test_choose_items_not_in_list(self):
        """
        choose_items_not_in_list() should choose a given number of items from a given list,
        such that the items are not in a given exclusion list.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = choose_items_not_in_list(item_list, excluded_items, 3)

        for i in results:
            self.assertIn(i, item_list)
            self.assertNotIn(i, excluded_items)

        non_dupes = list(set(results))
        self.assertEquals(len(non_dupes), len(results))


    def test_choose_items_not_in_list_just_enough(self):
        """
        choose_items_not_in_list() should choose a given number of items from a given list,
        such that the items are not in a given exclusion list.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = choose_items_not_in_list(item_list, excluded_items, 5)

        for i in results:
            self.assertIn(i, item_list)
            self.assertNotIn(i, excluded_items)

        non_dupes = list(set(results))
        self.assertEquals(len(non_dupes), len(results))


    def test_choose_items_not_in_list_not_enough_items(self):
        """
        If there are not enough items to form a list, choose_items_not_in_list() should
        return None.
        """
        item_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        excluded_items = [1, 3, 5, 7, 9]

        results = choose_items_not_in_list(item_list, excluded_items, 6)

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
    Hi
    """

    def test_call_rand_functions(self):
        """
        call_rand_functions() should accept a list of functions, a list of arguments, and the
        number of functions to call, 'num'. It should call these functions and collect their
        return values until the number of non-None return values is equal to 'num'. It should
        return a list of these non-None return values.

        Each function should be passed the arguments stored in the given arg list
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
        call_rand_functions() should also work if there are no arguments in the arg list.
        """
        functions = [func4, func5]
        args = []

        results = call_rand_functions(functions, args, 2)

        self.assertCountEqual(results, [1, 2])


    def test_call_rand_functions_zero_return(self):
        functions = [func0, func0]
        args = [0]

        results = call_rand_functions(functions, args, 1)

        self.assertCountEqual(results, [0])


    def test_call_rand_functions_not_enough_funcs(self):
        """
        call_rand_functions() should return None if there aren't enough functions to return
        the proper number of return values.
        """
        functions = [func0, func1, func2, func3]
        args = [3]

        results = call_rand_functions(functions, args, 5)

        self.assertIsNone(results)


    def test_call_rand_functions_funcs_return_none(self):
        """
        call_rand_functions() should return None if there are enough functions, but too many
        of them return None.
        """
        functions = [func0, func1, func2, func6, func6]
        args = [5]

        results = call_rand_functions(functions, args, 4)

        self.assertIsNone(results)



class CallRandFunctionsArgSetsTests(TestCase):
    """
    """

    def test_call_rand_functions_arg_sets(self):
        """
        call_rand_functions() should accept a list of functions, a list of arguments, and the
        number of functions to call, 'num'. It should call these functions and collect their
        return values until the number of non-None return values is equal to 'num'. It should
        return a list of these non-None return values.

        Each function should be passed the arguments stored in the given arg list
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
        functions = [func0, func0, func0]
        args = [[1], [2], [3]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertCountEqual(results, [1, 2, 3])


    def test_call_rand_functions_arg_sets_zero_return(self):
        functions = [func0, func0]
        args = [[0], [0]]

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertCountEqual(results, [0, 0])


    def test_call_rand_functions_arg_sets_no_args(self):
        """
        call_rand_functions() should also work if there are no arguments in the arg list.
        """
        functions = [func4, func5]
        args = []

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_not_enough_funcs(self):
        """
        call_rand_functions() should return None if there aren't enough functions to return
        the proper number of return values.
        """
        functions = [func0, func1, func2, func3]
        args = [[3], [4], [5], [6]]

        results = call_rand_functions_arg_sets(functions, args, 5)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_not_enough_arguments(self):
        functions = [func0, func1, func2, func3]
        args = [[3], [4], [5]]

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_funcs_return_none(self):
        """
        call_rand_functions() should return None if there are enough functions, but too many
        of them return None.
        """
        functions = [func0, func1, func2, func6, func6]
        args = [[3], [4], [5], [6], [7]]

        results = call_rand_functions_arg_sets(functions, args, 4)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_ensure_pairings(self):
        functions = [func0, func1, func2, func3]
        args = [[4], [3], [2], [1]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertCountEqual(results, [4, 4, 4])

