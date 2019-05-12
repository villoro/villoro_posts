"""
    Singleton loader. Calling sync for one instance will update all of them.
"""


data = {"value": 0}


def sync():
    # It is important to update the data variable instead of assign a new value
    # data = {"value": data.get("value", 0) + 1} won't work as expected
    data.update({"value": data.get("value", 0) + 1})


def get_value():
    return data.get("value", 0)
