class NotImplementedError(Exception):
    def __init__(self):
        self.value = "Not implemented"

    def __str__(self):
        return str(self.value)


class InvalidMove(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class InternalError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
