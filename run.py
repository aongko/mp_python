import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor


def do(something):
    print("Doing {}".format(something))
    sleep(random.uniform(2, 3))
    print("Done doing {}".format(something))


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.map(do, range(1000))
