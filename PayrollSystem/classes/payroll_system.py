class PayrollSystem:
    def __init__(self, list_of_employers=None):
        self.employers = list_of_employers or []

    def __str__(self):
        return f"{[str(employer) for employer in self.employers]}"

    def add_employer(self, new_employer):
        for employer in self.employers:
            if employer.employer_id == new_employer.employer_id:
                raise ValueError("List already contains this employer")
        self.employers.append(new_employer)

    def remove_employer(self, employer_id):
        for employer in self.employers:
            if employer.employer_id == employer_id:
                self.employers.remove(employer)
                return
        raise ValueError("Employer not found")

    def find_employer(self, employer_id):
        for employer in self.employers:
            if employer.employer_id == employer_id:
                return employer
        raise ValueError("Employer not found")

    def add_hours(self, employer_id, date, hours):
        for employer in self.employers:
            if employer_id == employer.employer_id:
                employer.add_hours(date, hours)
                return
        raise ValueError("Employer not found")

    def review(self, date):
        all_employers_review = []
        for employer in self.employers:
            employer_review = employer.review(date)
            employer_review["employer_id"] = employer.employer_id
            all_employers_review.append(employer_review)
        return all_employers_review

    def max_salary(self, date):
        max_salary, employer_id = 0, self.employers[0].employer_id if self.employers else None
        for employer in self.employers:
            if (salary := employer.salary(date)) > max_salary:
                max_salary = salary
                employer_id = employer.employer_id
        return employer_id
