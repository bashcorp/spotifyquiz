from django.test import TransactionTestCase, TestCase

from spoton.quiz.quiz import *


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
        args = [[3], [4], [5]]

        results = call_rand_functions_arg_sets(functions, args, 3)

        self.assertIsNotNone(results)

        poss_results = list(range(3, 6))
        for i in results:
            self.assertIn(i, poss_results)


    def test_call_rand_functions_arg_sets_no_args(self):
        """
        call_rand_functions() should also work if there are no arguments in the arg list.
        """
        functions = [func4, func5]
        args = []

        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertCountEqual(results, [1, 2])


    def test_call_rand_functions_arg_sets_one_arglist(self):
        """

        """
        functions = [func0, func0, func0]
        args = [[3]]
        
        results = call_rand_functions_arg_sets(functions, args, 2)

        self.assertCountEqual(results, [3, 3])


    def test_call_rand_functions_arg_sets_not_enough_funcs(self):
        """
        call_rand_functions() should return None if there aren't enough functions to return
        the proper number of return values.
        """
        functions = [func0, func1, func2, func3]
        args = [[3], [4]]

        results = call_rand_functions_arg_sets(functions, args, 5)

        self.assertIsNone(results)


    def test_call_rand_functions_arg_sets_funcs_return_none(self):
        """
        call_rand_functions() should return None if there are enough functions, but too many
        of them return None.
        """
        functions = [func0, func1, func2, func6, func6]
        args = [[5], [3]]

        results = call_rand_functions_arg_sets(functions, args, 4)

        self.assertIsNone(results)
