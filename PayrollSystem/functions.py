from pandas.core.dtypes.cast import ensure_dtype_can_hold_na

from classes.employer import *
from classes.payroll_system import *
import csv

def read_employers(filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def write(filename, items):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=sorted(items[0].keys()))
        writer.writeheader()
        writer.writerows(items)

def write_employer(filename, employer):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(employer))

def create_system(employers):
    system = []
    for employer in employers:
        system.append(
            Employer(
                int(employer["employer_id"]),
                employer["name"],
                employer["position"],
                int(employer["hourly_rate"])
            )
        )
    return PayrollSystem(system)