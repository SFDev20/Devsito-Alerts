def msToDate(ms, next_day=False):
    total_seconds = ms / 1000.0

    if next_day and (total_seconds % 86400) >= 86370:
        total_seconds += 300

    days = int(total_seconds // 86400)
    remaining = total_seconds % 86400
    hours = int(remaining // 3600)
    minutes = int((remaining % 3600) // 60)
    seconds = int(remaining % 60)

    return days, hours, minutes, seconds
