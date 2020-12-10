class TestCase(object):
    def __init__(self, case, expected):
        self.case = case
        self.expected = expected

    def check(self, actual):
        if self.expected == actual:
            case = repr(self.case).strip().replace(r'\n', ' ')
            print("OK %s %s%s" % (self.expected, case[:100], '...' if len(case) > 100 else ''))
        else:
            print("FAIL %s, expected %s, got %s" % (self.case, self.expected, actual))
