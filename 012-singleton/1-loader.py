"""
    Simple loader that will only update the value of the current instance
"""


class loader:
    def __init__(self):
        self.value = 0

    def sync(self):
        """ This will only sync the current instance """
        self.value += 1

    def get_value(self):
        return self.value


if __name__ == "__main__":
    loader1 = loader()
    loader2 = loader()

    loader1.sync()
    print(loader1.get_value())

    print(loader2.get_value())
