"""
    Mixing both types of class instances
"""


class mloader:

    value = 0

    def sync(self, new_value):
        """
            This will only sync the current instance.
            If you use that one time the sync all won't work
        """
        self.value = new_value

    @staticmethod
    def sync_all(new_value):
        """ This will update the value in ALL instances"""
        mloader.value = new_value

    def get_value(self):
        return self.value


if __name__ == "__main__":

    mloader_1 = mloader()
    mloader_2 = mloader()

    mloader.sync_all(5)
    print(f"Loader_1: {mloader_1.get_value()}. Loader_2: {mloader_2.get_value()}")

    mloader_1.sync(2)
    print(f"Loader_1: {mloader_1.get_value()}. Loader_2: {mloader_2.get_value()}")

    mloader.sync_all(7)
    print(f"Loader_1: {mloader_1.get_value()}. Loader_2: {mloader_2.get_value()}")
