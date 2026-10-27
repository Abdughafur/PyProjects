# Created by Abdughafur

import calendar


# =============================A===============================
# PYCALENDAR
# ============================================================

def display_calendar(year, month):
    """Display a formatted calendar for one month."""

    month_name = calendar.month_name[month]

    print()
    print("=" * 32)
    print(f"📅 {month_name.upper()} {year}")
    print("=" * 32)
    print(calendar.month(year, month))


def get_year():
    """Ask for a positive calendar year."""

    while True:
        value = input("Enter year: ").strip()

        try:
            year = int(value)
        except ValueError:
            print("❌ Please enter a whole number for the year.")
            continue

        if year < 1:
            print("❌ Year must be greater than 0.")
            continue

        return year


def get_month():
    """Ask for a month number from 1 to 12."""

    while True:
        value = input("Enter month number (1-12): ").strip()

        try:
            month = int(value)
        except ValueError:
            print("❌ Please enter a whole number from 1 to 12.")
            continue

        if not 1 <= month <= 12:
            print("❌ Month must be between 1 and 12.")
            continue

        return month


def main():
    year = get_year()
    month = get_month()
    display_calendar(year, month)


if __name__ == "__main__":
    main()