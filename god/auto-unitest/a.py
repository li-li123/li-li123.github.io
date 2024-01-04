from datetime import datetime


if __name__ == '__main__':
    start_time = datetime(2021, 8, 1, 10, 12, 34)
    end_time = datetime(2021, 8, 2, 13, 45, 56)

    time_diff = end_time - start_time

    print(time_diff.minute)