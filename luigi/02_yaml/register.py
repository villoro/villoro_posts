from datetime import date, datetime


def main(filename):

    uri = f"output/{filename}.txt"

    with open(uri, "w") as stream:
        # This will fail on purpouse to see how Luigi handles errors
        stream.write(datetime.now().worngtime("%Y-%m-%d %H:%M:%S"))

    print(f"File '{uri}' wrote")


if __name__ == "__main__":
    main(date.today().strftime("%Y_%m_%d"))
