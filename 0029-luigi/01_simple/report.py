from datetime import date, datetime
from markdown import markdown


def main(filename):

    uri = f"output/{filename}.html"

    html = markdown(
        f"""# Report
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
    )

    with open(uri, "w") as stream:
        stream.write(html)

    print(f"File '{uri}' wrote")


if __name__ == "__main__":
    main(date.today().strftime("%Y_%m_%d"))
