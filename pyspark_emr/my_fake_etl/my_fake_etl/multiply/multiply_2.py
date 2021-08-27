from my_fake_etl.multiply.functions import get_args

from loguru import logger


def main():

    num = get_args()

    logger.info(f"Result is {num*2}")


if __name__ == "__main__":
    main()
