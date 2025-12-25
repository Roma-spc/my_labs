from classes.class_functions import *

class Employer:
    def __init__(self, employer_id, name, position, hourly_rate):
        self.employer_id = employer_id
        self.name= name
        self.position = position
        self.hourly_rate = hourly_rate
        self.hours_per_month = {}

    def __str__(self):
        return f"id: {self.employer_id}\nname: {self.name}\nposition: {self.position}\nhourly rate: {self.hourly_rate}"

    def add_hours(self, date, hours):
        if check_date(date):
            if date in self.hours_per_month:
                self.hours_per_month[date] += hours
            else:
                self.hours_per_month[date] = hours
        else:
            raise ValueError("Invalid str format YYYY-MM")


    def salary(self, date):
        if check_date(date):
            return self.hours_per_month.get(date, 0) * self.hourly_rate
        raise ValueError("Invalid str format YYYY-MM")

    def review(self, date):
        return {
            "hours": self.hours_per_month.get(date, 0),
            "salary": self.salary(date)
        }

