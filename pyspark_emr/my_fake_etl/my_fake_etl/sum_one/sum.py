from my_fake_etl.sum_one.functions import get_args

from loguru import logger


def sum_one(num):

    logger.info(f"Result is {num + 1}")


def main():

    num = get_args()

    sum_one(num)


if __name__ == "__main__":
    main()
