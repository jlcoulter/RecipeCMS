"""ISO 8601 duration parsing helpers."""

import re


def iso8601_to_human_readable(duration_str):
    """Convert an ISO 8601 duration string to a human-readable string."""
    try:
        pattern = r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?"
        match = re.match(pattern, duration_str)
        if not match:
            return "Invalid ISO 8601 duration string"

        years, months, days, hours, minutes, seconds = match.groups()

        duration_parts = []
        if years:
            duration_parts.append(f"{years} year{'s' if int(years) != 1 else ''}")
        if months:
            duration_parts.append(f"{months} month{'s' if int(months) != 1 else ''}")
        if days:
            duration_parts.append(f"{days} day{'s' if int(days) != 1 else ''}")
        if hours:
            duration_parts.append(f"{hours} hour{'s' if int(hours) != 1 else ''}")
        if minutes:
            duration_parts.append(f"{minutes} minute{'s' if int(minutes) != 1 else ''}")
        if seconds:
            duration_parts.append(f"{seconds} second{'s' if int(seconds) != 1 else ''}")

        return ", ".join(duration_parts)

    except ValueError:
        return "Invalid ISO 8601 duration string"


def iso8601_to_seconds(duration_str):
    """Convert an ISO 8601 duration string to total seconds."""
    try:
        pattern = r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?"
        match = re.match(pattern, duration_str)
        if not match:
            return "Invalid ISO 8601 duration string"

        years, months, days, hours, minutes, seconds = match.groups()
        total_seconds = 0
        if years:
            total_seconds = total_seconds + (int(years) * 31556926)
        if months:
            total_seconds = total_seconds + (int(months) * 2629746)
        if days:
            total_seconds = total_seconds + (int(days) * 86400)
        if hours:
            total_seconds = total_seconds + (int(hours) * 3600)
        if minutes:
            total_seconds = total_seconds + (int(minutes) * 60)
        if seconds:
            total_seconds = total_seconds + int(seconds)

        return total_seconds

    except ValueError:
        return "Invalid ISO 8601 duration string"