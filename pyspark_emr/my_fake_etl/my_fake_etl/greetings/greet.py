from my_fake_etl.greetings.functions import get_args

from loguru import logger


def greet(greeting_word, name):

    logger.info(f"{greeting_word} {name}")


def main():

    name, greeting_word = get_args()

    greet(greeting_word, name)


if __name__ == "__main__":
    main()
