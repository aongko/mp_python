import random
from time import sleep


def do(something):
    print("Doing {}".format(something))
    sleep(random.uniform(2, 3))
    print("Done doing {}".format(something))


if __name__ == "__main__":
    for i in range(1000):
        do(i)
