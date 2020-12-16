class TestCase(object):
    def __init__(self, case, expected):
        self.case = case
        self.expected = expected

    @staticmethod
    def _format_case(case):
        case = repr(case).strip().replace(r'\n', ' ')
        return case[:97] + ('...' if len(case) > 100 else '')

    def check(self, actual):
        if self.expected == actual:
            print("OK %s %s" % (self.expected, self._format_case(self.case)))
        else:
            print("FAIL expected %s, got %s, %s" % (self.expected, actual, self._format_case(self.case)))
