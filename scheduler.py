from tasks import do


if __name__ == "__main__":
    for i in range(1000):
        do.delay(i)
