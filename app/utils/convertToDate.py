from datetime import timedelta


def msToDate(ms):
    seconds = int(ms) // 1000
    td = timedelta(seconds=seconds)

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return days, hours, minutes, seconds
