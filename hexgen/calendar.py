import math
import random


class Month:
    def __init__(self, ordinal, num_days, day_length):
        self.ordinal = ordinal
        self.num_days = num_days
        self.day_length = day_length

    def __repr__(self):
        return "<Month ordinal={} " "num_days={} " "day_length={}>".format(self.ordinal, self.num_days, self.day_length)


class Calendar:
    def __init__(self, year_length, day_length, month_length_target=None):
        self.year_length = year_length
        self.day_length = day_length

        self.months = []

        # determine the number of months
        # split the year_length into twelve months with an integer number of days
        # each month should have around 30 days
        if month_length_target is None:
            if year_length > 35:
                month_length_target = random.randint(25, 35)
            else:
                month_length_target = year_length / 2

        found_month_number = year_length
        num_months = found_month_number
        while math.floor(year_length / found_month_number) < month_length_target:
            num_months = found_month_number
            found_month_number -= 1
        even_split = year_length / num_months

        days_left = year_length
        even_split = math.floor(even_split)
        for num in range(1, num_months + 1):
            if days_left - even_split < even_split:
                num_days = days_left
            else:
                num_days = even_split
            self.months.append(Month(num, num_days, day_length))
            days_left -= even_split
