import inspect


class Case(object):
    def __init__(self, arg, result):
        self.arg = arg
        self.result = result

    def assert_it(self, test_case, func):
        if inspect.isclass(self.result) and isinstance(
            self.result(), Exception
        ):
            test_case.assertRaises(self.result, func, self.arg)
        else:
            test_case.assertEqual(func(self.arg), self.result, self.arg)
