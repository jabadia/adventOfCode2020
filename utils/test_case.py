class TestCase(object):
    def __init__(self, case, expected):
        self.case = case
        self.expected = expected

    def check(self, actual):
        if self.expected == actual:
            print("OK %s" % (self.case,))
        else:
            print("FAIL %s, expected %s, got %s" % (self.case, self.expected, actual))
