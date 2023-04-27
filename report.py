from collections import defaultdict
from datetime import datetime
from datetime import timedelta

import click
import icalendar
import requests
from tabulate import tabulate


def check_offset(ctx, param, value):
    if value > 0:
        raise click.BadParameter("needs to be 0 or less")
    return value


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("month_offset", default=0, type=int, callback=check_offset)
def report(month_offset):
    with open(".secret") as s:
        SECRET_URL = s.read().strip()

    data = requests.get(SECRET_URL).content
    calendar = icalendar.Calendar.from_ical(data)

    selected_month = datetime(
        datetime.now().year + ((datetime.now().month + month_offset) // 12),
        (datetime.now().month + month_offset) % 12,
        1,
    )

    duration_by_day = defaultdict(lambda: defaultdict(timedelta))
    for component in calendar.walk():
        if component.name == "VEVENT":
            start_time = component.get("DTSTART").dt
            if (
                start_time.year != selected_month.year
                or start_time.month != selected_month.month
            ):
                continue
            end_time = component.get("DTEND").dt
            duration = end_time - start_time
            day = start_time.date()
            label = component.get("SUMMARY")
            duration_by_day[day][label] += duration

    rows = []
    for day, durations in sorted(duration_by_day.items()):
        for label, duration in durations.items():
            rows.append([day.strftime("%Y-%m-%d"), label, str(duration)])
    print(tabulate(rows, headers=["Date", "Summary", "Duration"]))


if __name__ == "__main__":
    report()
