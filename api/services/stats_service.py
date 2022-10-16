import csv
from typing import List

import pandas as pd
import os
import pprint


def main():
    """
    Invokes the methods from this service and generates a dict with this format:

        {
            "stats":{
                "histogram_data":[ 
                    {
                        "price_range":"0-50",
                        "count":2 },
                    {
                        "price_range":"51-100", 
                        "count":143
                    }, 
                    {
                        "price_range":"101-150",
                        "count":28 
                    },
                    {
                        "price_range":"150-max", 
                        "count":28
                    } ],
                "pie_chart_data":[ 
                    {
                        "room_type":"Private room",
                        "count":150 },
                    {
                        "room_type":"Entire home/apt", 
                        "count":50
                    } ],
                "bar_char_data":[ 
                    {
                        "neighborhood":"Centrum-West",
                        "avg_price":120.3 },
                    {
                        "neighborhood":"Slotervaart", 
                        "avg_price":81
                    } ]
                }
            }
    :return:
    
    """
    job_stats = max_min_per_job()
    department_stats = avg_salary_emp_count_per_department()
    return {"data": {"job_stats": job_stats, "department_stats": department_stats}}


def max_min_per_job() -> List[dict]:
    """
    Calculates the min and max salary for each job and also counts its occurents.

    :return: List of dicts to be used to the exposed response
    """
    employee_dataframe = pd.read_csv(os.getcwd() + "/repo/curated_employees.csv")

    stats_df = employee_dataframe.groupby(["job"]).agg(
        {"job": "job", "job": ["count"], "salary": ["min", "max"]}
    )

    s = stats_df.to_dict("index")
    job_stats = []
    for k, v in s.items():
        job_stat = {
            "job": k,
            "stats": {"job_count": 0, "min_salary": 0, "max_salary": 0},
        }
        job_stat["stats"]["job_count"] = v[("job", "count")]
        job_stat["stats"]["min_salary"] = v[("salary", "min")]
        job_stat["stats"]["max_salary"] = v[("salary", "max")]
        job_stats.append(job_stat)
    return job_stats


def avg_salary_emp_count_per_department():
    """
    Calculates the avg salary and the employee count for each department.

    :return: List of dicts to be used to the exposed response
    """
    employee_dataframe = pd.read_csv(os.getcwd() + "/repo/curated_employees.csv")

    stats_df = employee_dataframe.groupby(["department"]).agg(
        {"id": ["count"], "salary": ["mean"]}
    )

    s = stats_df.to_dict("index")
    department_stats = []
    for k, v in s.items():
        department = {
            "department": k,
            "stats": {"employee_count": 0, "mean_salary": 0},
        }
        department["stats"]["employee_count"] = v[("id", "count")]
        department["stats"]["mean_salary"] = v[("salary", "mean")]
        department_stats.append(department)
    return department_stats


def calculate_average_salary() -> float:
    """
    Calculates the average salary to fill missing values during ETL pipeline.

    :return: float: the avg salary
    """
    employee_dataframe = pd.read_csv(os.getcwd() + "/repo/curated_employees.csv")

    return round(float(employee_dataframe["salary"].mean()), 2)


# Add here any other functions that you want to generate more stats and then add them in the response in main

