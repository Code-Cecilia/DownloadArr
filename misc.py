def camel_to_sentence(camel_case, replacements=None):
    if replacements is None:
        replacements = {}

    for key, value in replacements.items():
        camel_case = camel_case.replace(key, value)  # replace all the keys with the values
    final_string = ""
    for char in camel_case:
        if char.isupper():
            final_string += " " + char.lower()
        else:
            final_string += char
    return final_string.title()


def pretty_time_remaininf(time_remaining_seconds):
    if time_remaining_seconds <= 0:
        return "0 seconds"
    minutes, seconds = divmod(time_remaining_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    final_string_to_join = []
    if weeks > 0:
        final_string_to_join.append(f"{weeks} {'weeks' if weeks != 1 else 'week'}")
    if days > 0:
        final_string_to_join.append(f"{days} {'days' if days != 1 else 'day'}")
    if hours > 0:
        final_string_to_join.append(f"{hours} {'hours' if hours != 1 else 'hour'}")
    if minutes > 0:
        final_string_to_join.append(f"{minutes} {'minutes' if minutes != 1 else 'minute'}")
    if seconds > 0:
        final_string_to_join.append(f"{seconds} {'seconds' if seconds != 1 else 'second'}")

    final_string = ", ".join(final_string_to_join)
    return final_string


def bytespersec_to_megabytespersec(bps):
    return bps / 1000000


def bytes_to_nearest(bytes):
    if 1 < bytes < 1024:
        return f"{bytes} B"

    kilobytes = bytes / 1000
    if 1 < kilobytes < 1000:
        return f"{round(kilobytes, 1)} KB"

    megabytes = kilobytes / 1000
    if 1 < megabytes < 1000:
        return f"{round(megabytes, 1)} MB"

    gigabytes = megabytes / 1000
    if 1 < gigabytes < 1000:
        return f"{round(gigabytes, 1)} GB"

    terabytes = gigabytes / 1000
    if 1 < terabytes < 1000:
        return f"{round(terabytes, 1)} TB"
