from functions import *
import random

INPUT_DATA_DIR = "input_data"
RESULT_DIR = "results"

payroll_system = create_system(read_employers(f"{INPUT_DATA_DIR}/employers.csv"))


for employer_id in range(1, 7):
    random_number = random.randint(100, 200)

    payroll_system.add_hours(employer_id, "2025-12", random_number)

write(f"{RESULT_DIR}/review.csv", payroll_system.review("2025-12"))

payroll_system.remove_employer(6)

id_max_salary = payroll_system.max_salary("2025-12")

write_employer(f"{RESULT_DIR}/max_salary.txt", payroll_system.find_employer(id_max_salary))


