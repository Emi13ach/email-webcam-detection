from datetime import datetime


def get_day():
    now = datetime.now()
    dt_str = now.strftime("%A")
    return dt_str


def get_time():
    now = datetime.now()
    dt_str = now.strftime("%H:%M:%S")
    return dt_str


if __name__ == "__main__":
    print(get_time())
