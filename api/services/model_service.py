import os
from csv import reader, DictWriter

import requests

from emp_base_logger import logger


def main():
    """
    Orchestrates the transformation for each employee by invoking any relevant function and stores them in a new file.

    :return:
    """
    employee_data = retrieve_data()
    curated_employee_data = []

    roe_to_use = get_roe_from_external_service()

    for employee in employee_data:
        curated_employee = dict.fromkeys(
            [
                "id",
                "full_name",
                "email",
                "gender",
                "title",
                "salary",
                "job",
                "department",
            ]
        )
        curated_employee["id"] = int(employee[0])
        curated_employee["full_name"] = transform_name(employee[1], employee[2])
        curated_employee["email"] = transform_email(employee[1], employee[2])
        curated_employee["gender"] = transform_gender(employee[4])
        curated_employee["title"] = transform_title(curated_employee["gender"])
        curated_employee["salary"] = convert_salary_to_euro(employee[-1], roe_to_use)
        curated_employee["job"] = employee[-3]
        curated_employee["department"] = employee[-4]

        curated_employee_data.append(curated_employee)

    try:
        save_to_file(curated_employee_data)
        return {"completed": True}
    except Exception as exception:
        logger.error(f"Could not run etl on employees {exception}")

        return {"completed": False}


def retrieve_data():
    with open(os.getcwd() + "/repo/employees.csv", "r+") as emp_file:
        employee_data = reader(emp_file)
        next(employee_data)

        return list(employee_data)


def transform_name(first_name, last_name):
    return first_name + " " + last_name


def transform_email(first_name, last_name):
    return first_name[0].lower() + "." + last_name.lower() + "@lorempipsum.com"


def transform_gender(gender_initial):
    if gender_initial == "M":
        return "Male"
    return "Female"


def transform_title(gender):
    if gender == "Male":
        return "Mr"
    return "Mrs"


def convert_salary_to_euro(salary_in_usd, roe):
    return round(float(salary_in_usd) * float(roe), 2)


def save_to_file(data):
    #  without newline u get blank lines

    with open(os.getcwd() + "/repo/curated_employees.csv", "w+", newline="") as new_emp_file:
        fieldnames = data[0].keys()

        writer = DictWriter(new_emp_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_roe_from_external_service() -> float:
    """
    Attempts to get the rate of exchange from a third party service.
    If that does not work, it will return by default 0.88

    NOTE: This API is not free so this is here just for demo purposes.

    :return: float the roe for USD->EUR conversion
    """

    response = requests.get("https://api.exchangeratesapi.io/latest?base=USD")
    rsp = response.json()
    if response.status_code != 200:
        return 0.88
    return rsp.get("rates", {}).get("EUR", 0.88)