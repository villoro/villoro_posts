from datetime import date, datetime


def do(filename):

    uri = f"output/{filename}.txt"

    with open(uri, "w") as stream:
        stream.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print(f"File '{uri}' wrote")


if __name__ == "__main__":
    do(date.today().strftime("%Y_%m_%d"))
