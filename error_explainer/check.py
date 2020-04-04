class Check:
    """
    Wrapper class for holding the level and function of a check.
    """

    def __init__(self, level, function):
        self.level = level
        self.function = function

    def run(self, *kwargs):
        self.function(*kwargs)
