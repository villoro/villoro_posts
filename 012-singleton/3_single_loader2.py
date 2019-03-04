"""
    Singleton loader. Calling sync for one instance will update all of them.
"""


class single_loader2:

    value = 0

    @staticmethod
    def sync_all():
        """ This will update the value in ALL instances"""
        single_loader2.value += 1

    def get_value(self):
        return self.value


if __name__ == "__main__":

    loader1 = single_loader2()
    loader2 = single_loader2()

    single_loader2.sync_all()  # It is a staticmethod, you can call directly the class function

    print(loader1.get_value())
    print(loader2.get_value())
