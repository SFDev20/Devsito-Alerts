from datetime import timedelta


def msToDate(ms, next_day=False):
    seconds = int(ms) // 1000
    td = timedelta(seconds=seconds)

    # Si estamos aún en hora 23, asumimos que falta poco para el siguiente día
    if next_day:
        hours, _ = divmod(td.seconds, 3600)
        if hours == 23:
            td += timedelta(minutes=5)

    # Recalcula después del posible ajuste
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    remaining = total_seconds % 86400
    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60

    return days, hours, minutes, seconds
