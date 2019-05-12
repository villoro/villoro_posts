"""
    Test the single_loader.py
"""

import single_loader

if __name__ == "__main__":

    single_loader1 = single_loader
    single_loader2 = single_loader

    single_loader1.sync()
    print(single_loader1.get_value())

    print(single_loader2.get_value())
