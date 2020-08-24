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
