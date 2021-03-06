# required imports
from ortools.sat.python import cp_model

import array as arr
import numpy as np
import time

def main():

    #Start timing
    time_start = time.time()

    # 0.) Define input:
    # 0.1) Define number of employees / jobs / qualifications / days / shifts per day
    #!!ATTENTION: when adjusting the numbers, be careful to also adjust certain parts of the code (see following comments)
    number_employees: int = 50
    number_jobs: int = 30
    number_qualifications: int = 3
    number_days: int = 5

    number_shifts_per_day: int = 2
    number_total_shifts = number_days * number_shifts_per_day

    # 0.2) Define individual working hours per employee
    # for each employee an individual maximum shift is assigned, i creates array of integers
    # !!ATTENTION: MAX SHIFTS PER EMPLOYEE NEEDS TO BE ADJUSTED TO DAYS AND NUMBER SHIFTS PER DAY
    # !!ATTENTION: array lengths needs to be adjusted to number of employees
    #otherwise max shifts might not be sufficient to cover the required total number of shifts
    max_shifts_per_employee = arr.array('i', [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, 10, 10, 10, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, 10, 10, 10, 8, 10, 10, 10, 10])
    min_shifts_per_employee = arr.array('i', [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 2, 4, 4, 5, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 2, 4, 4, 5, 3, 4, 4, 4, 4, 4])

    # 0.3) Definition of Availability Matrix: Availability of each employee for each shift (number total shifts)
    # each line = one employee, each column = one shift of the total number of shifts (days * shifts per day)
    # 1 represents an available employee, 0 represents an absent employee who thus can not be assigned to a job
    # !!ATTENTION: Matrix NEEDS TO BE ADJUSTED TO DAYS AND NUMBER SHIFTS PER DAY (=number of columns)
    # !!ATTENTION: Matrix needs to be adjusted to number of employees (=number of lines)
    employee_availability_matrix = np.array([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                             [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                             [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                                             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                             [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                             [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                                             ])

    # 0.4) Definition of employee qualification matrix:
    # each line = one employee, each column = one qualification assessed on a scale from 1 to 3
    # 1 represents high skill, 3 represents low skill
    # !!ATTENTION: Matrix needs to be adjusted to number of employees (=number of lines)
    # !!ATTENTION: Matrix also needs to be adjusted to number of qualifications (=number of columns)
    employee_qualification_matrix = np.array([[1, 1, 2],
                                              [2, 1, 1],
                                              [3, 1, 2],
                                              [2, 3, 3],
                                              [2, 1, 2],
                                              [1, 1, 2],
                                              [2, 1, 1],
                                              [3, 1, 2],
                                              [2, 2, 3],
                                              [2, 1, 2],
                                              [1, 1, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [2, 2, 2],
                                              [2, 1, 1],
                                              [2, 2, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [1, 1, 1],
                                              [3, 2, 1],
                                              [2, 2, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [1, 1, 2],
                                              [2, 1, 1],
                                              [3, 1, 2],
                                              [2, 3, 3],
                                              [2, 1, 2],
                                              [1, 1, 2],
                                              [2, 1, 1],
                                              [3, 1, 2],
                                              [2, 2, 3],
                                              [2, 1, 2],
                                              [1, 1, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [2, 2, 2],
                                              [2, 1, 1],
                                              [2, 2, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [1, 1, 1],
                                              [3, 2, 1],
                                              [2, 2, 2],
                                              [1, 1, 1],
                                              [3, 3, 3],
                                              [1, 1, 1],
                                              [3, 3, 3]
                                              ])
    # 0.5) Definition of Job Requirements Matrix
    # each line = one job, each column = one qualification assessed on a scale from 1 to 3
    # !!ATTENTION: Matrix needs to be adjusted to number of jobs (=number of lines)
    # and number of qualifications (=number of columns)
    job_required_qualification_matrix = np.array([[3, 3, 3],
                                                  [2, 1, 2],
                                                  [3, 2, 2],
                                                  [3, 2, 2],
                                                  [3, 3, 3],
                                                  [2, 2, 2],
                                                  [3, 2, 2],
                                                  [3, 3, 3],
                                                  [1, 1, 2],
                                                  [1, 2, 3],
                                                  [3, 3, 3],
                                                  [1, 1, 1],
                                                  [3, 3, 3],
                                                  [3, 3, 3],
                                                  [2, 1, 2],
                                                  [3, 3, 3],
                                                  [2, 1, 2],
                                                  [3, 2, 2],
                                                  [3, 2, 2],
                                                  [3, 3, 3],
                                                  [2, 2, 2],
                                                  [3, 2, 2],
                                                  [3, 3, 3],
                                                  [1, 1, 2],
                                                  [1, 2, 3],
                                                  [3, 3, 3],
                                                  [1, 1, 1],
                                                  [3, 3, 3],
                                                  [3, 3, 3],
                                                  [2, 1, 2],
                                                  ])

    # 0.6) Definition of Employee-Job Matrix
    x = (number_employees, number_jobs)
    # creates array of the size number employees x number of jobs mit zeros
    # later on it will be calculated in this matrix which job can be done by which employee based on their qualifications
    # and the required job qualifications -->see step 4.3
    employee_job_calculation_matrix = np.zeros(x, dtype=int)

    # 0.7) Definition of Employee-Job Preference Matrix
    # each line = one employee, each column = one job assessed on a scale from 0 to 100
    # 100 represents highest preference, 0 represents lowest preference
    # -->thus later on total preference score is maximized
    employee_job_preference_matrix = np.array([[50, 20, 15, 30, 55, 80, 60, 45, 30, 20, 20, 0, 60, 50, 45, 50, 20, 15, 30, 55, 80, 60, 45, 30, 20, 20, 0, 60, 50, 45],
                                               [0, 100, 50, 20, 100, 35, 0, 10, 50, 0, 0 , 0, 0, 15, 35, 0, 100, 50, 20, 100, 35, 0, 10, 50, 0, 0 , 0, 0, 15, 35],
                                               [90, 25, 45, 25, 65, 25, 35, 80, 25, 50, 30, 20, 20, 20, 30, 90, 25, 45, 25, 65, 25, 35, 80, 25, 50, 30, 20, 20, 20, 30],
                                               [65, 50, 15, 0, 0, 90, 70, 50, 20, 80, 75, 15, 50, 50, 65, 65, 50, 15, 0, 0, 90, 70, 50, 20, 80, 75, 15, 50, 50, 65],
                                               [50, 50, 60, 10, 90, 0, 80, 30, 0, 55, 45, 35, 80, 65, 60, 50, 50, 60, 10, 90, 0, 80, 30, 0, 55, 45, 35, 80, 65, 60],
                                               [50, 20, 15, 35, 80, 65, 10, 10, 55, 0, 15, 70, 70, 50, 0, 50, 20, 15, 35, 80, 65, 10, 10, 55, 0, 15, 70, 70, 50, 0],
                                               [20, 20, 20, 45, 20, 0, 10, 90, 30, 80, 70, 35, 90, 75, 30, 20, 20, 20, 45, 20, 0, 10, 90, 30, 80, 70, 35, 90, 75, 30],
                                               [65, 90, 75, 50, 30, 80, 0, 90, 100, 90, 80, 0, 75, 60, 35, 65, 90, 75, 50, 30, 80, 0, 90, 100, 90, 80, 0, 75, 60, 35],
                                               [10, 45, 60, 80, 70, 50, 0, 35, 45, 0, 75, 65, 50, 60, 30, 10, 45, 60, 80, 70, 50, 0, 35, 45, 0, 75, 65, 50, 60, 30],
                                               [15, 20, 80, 90, 40, 50, 90, 45, 15, 10, 80, 75, 75, 65, 40, 15, 20, 80, 90, 40, 50, 90, 45, 15, 10, 80, 75, 75, 65, 40],
                                               [50, 50, 60, 100, 90, 0, 80, 30, 0, 0, 15, 25, 45, 60, 15, 50, 50, 60, 100, 90, 0, 80, 30, 0, 0, 15, 25, 45, 60, 15],
                                               [50, 20, 90, 35, 80, 65, 10, 10, 75, 80, 60, 50, 80, 65, 35, 50, 20, 90, 35, 80, 65, 10, 10, 75, 80, 60, 50, 80, 65, 35],
                                               [20, 20, 20, 45, 20, 40, 10, 80, 30, 35, 20, 35, 20, 10, 0, 20, 20, 20, 45, 20, 40, 10, 80, 30, 35, 20, 35, 20, 10, 0],
                                               [0, 35, 45, 55, 30, 60, 0, 40, 0, 35, 40, 50, 0, 0, 60, 0, 35, 45, 55, 30, 60, 0, 40, 0, 35, 40, 50, 0, 0, 60],
                                               [10, 65, 70, 70, 70, 70, 60, 55, 45, 70, 65, 35, 10, 55, 35, 10, 65, 70, 70, 70, 70, 60, 55, 45, 70, 65, 35, 10, 55, 35],
                                               [50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80, 50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80],
                                               [0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55, 0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55],
                                               [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70],
                                               [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 25, 30, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 25, 30],
                                               [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                                               [50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80, 50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80],
                                               [0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55, 0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55],
                                               [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
                                               [0, 40, 60, 0, 80, 0, 20, 0, 10, 0, 10, 0, 15, 25, 30, 0, 40, 60, 0, 80, 0, 20, 0, 10, 0, 10, 0, 15, 25, 30],
                                               [75, 100, 60, 0, 0, 100, 60, 40, 100, 50, 100, 35, 25, 35, 50, 75, 100, 60, 0, 0, 100, 60, 40, 100, 50, 100, 35, 25, 35, 50],
                                               [50, 20, 15, 30, 55, 80, 60, 45, 30, 20, 20, 0, 60, 50, 45, 50, 20, 15, 30, 55, 80, 60, 45, 30, 20, 20, 0, 60, 50, 45],
                                               [0, 100, 50, 20, 100, 35, 0, 10, 50, 0, 0, 0, 0, 15, 35, 0, 100, 50, 20, 100, 35, 0, 10, 50, 0, 0, 0, 0, 15, 35],
                                               [90, 25, 45, 25, 65, 25, 35, 80, 25, 50, 30, 20, 20, 20, 30, 90, 25, 45, 25, 65, 25, 35, 80, 25, 50, 30, 20, 20, 20, 30],
                                               [65, 50, 15, 0, 0, 90, 70, 50, 20, 80, 75, 15, 50, 50, 65, 65, 50, 15, 0, 0, 90, 70, 50, 20, 80, 75, 15, 50, 50, 65],
                                               [50, 50, 60, 10, 90, 0, 80, 30, 0, 55, 45, 35, 80, 65, 60, 50, 50, 60, 10, 90, 0, 80, 30, 0, 55, 45, 35, 80, 65, 60],
                                               [50, 20, 15, 35, 80, 65, 10, 10, 55, 0, 15, 70, 70, 50, 0, 50, 20, 15, 35, 80, 65, 10, 10, 55, 0, 15, 70, 70, 50, 0],
                                               [20, 20, 20, 45, 20, 0, 10, 90, 30, 80, 70, 35, 90, 75, 30, 20, 20, 20, 45, 20, 0, 10, 90, 30, 80, 70, 35, 90, 75, 30],
                                               [65, 90, 75, 50, 30, 80, 0, 90, 100, 90, 80, 0, 75, 60, 35, 65, 90, 75, 0, 30, 80, 0, 90, 100, 90, 80, 0, 75, 60, 35],
                                               [10, 45, 60, 80, 70, 50, 0, 35, 45, 0, 75, 65, 50, 60, 30, 10, 45, 60, 80, 70, 50, 0, 35, 45, 0, 75, 65, 50, 60, 30],
                                               [15, 20, 80, 90, 40, 50, 90, 45, 15, 10, 80, 75, 75, 65, 40, 15, 20, 80, 90, 40, 50, 90, 45, 15, 10, 80, 75, 75, 65, 40],
                                               [50, 50, 60, 100, 90, 0, 80, 30, 0, 0, 15, 25, 45, 60, 15, 50, 50, 60, 100, 90, 0, 80, 30, 0, 0, 15, 25, 45, 60, 15],
                                               [50, 20, 90, 35, 80, 65, 10, 10, 75, 80, 60, 50, 80, 65, 35, 50, 20, 90, 35, 80, 65, 10, 10, 75, 80, 60, 50, 80, 65, 35],
                                               [20, 20, 20, 45, 20, 40, 10, 80, 30, 35, 20, 35, 20, 10, 0, 20, 20, 20, 45, 20, 40, 10, 80, 30, 35, 20, 35, 20, 10, 0],
                                               [0, 35, 45, 55, 30, 60, 0, 40, 0, 35, 40, 50, 0, 0, 60, 0, 35, 45, 55, 30, 60, 0, 40, 0, 35, 40, 50, 0, 0, 60],
                                               [10, 65, 70, 70, 70, 70, 60, 55, 45, 70, 65, 35, 10, 55, 35, 10, 65, 70, 70, 70, 70, 60, 55, 45, 70, 65, 35, 10, 55, 35],
                                               [50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80, 50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80],
                                               [0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55, 0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55],
                                               [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70],
                                               [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 25, 30, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 25, 30],
                                               [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,100, 100],
                                               [50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80, 50, 70, 20, 55, 70, 40, 0, 0, 30, 75, 20, 85, 0, 60, 80],
                                               [0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55, 0, 35, 45, 0, 30, 60, 0, 0, 0, 35, 40, 0, 0, 50, 55],
                                               [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
                                               [0, 40, 60, 0, 80, 0, 20, 0, 10, 0, 10, 0, 15, 25, 30, 0, 40, 60, 0, 80, 0, 20, 0, 10, 0, 10, 0, 15, 25, 30],
                                               [75, 100, 60, 0, 0, 100, 60, 40, 100, 50, 100, 35, 25, 35, 50, 75, 100, 60, 0, 0, 100, 60, 40, 100, 50, 100, 35, 25, 35, 50]
                                               ])

    # 0.8) Definition of Employee-Job Preference Matrix
    #each employee has an individual "preference" (independent of the job_preference_matrix!!) for rotation
    #here: definition of rotation is how maximum often an employee wants to do a certain job in the schedule
    #thus: the lower the score, the higher the preference for rotation
    #but: if the score is set too low, there might be no solution anymore e.g. 1 would mean an employee
    #wants to do a job maximum one time -->will be difficult to find a solution
    rotation_preference_per_employee = arr.array('i', [3, 3, 3, 3, 4, 4, 3, 2, 4, 6, 5, 2, 3, 3, 3, 2, 4, 4, 4, 3, 3, 2, 4, 4, 3, 3, 3, 3, 3, 4, 4, 3, 2, 4, 6, 5, 2, 3, 3, 3, 2, 4, 4, 4, 3, 3, 2, 4, 4, 3])

    # each variable is assigned a range
    employees = range(number_employees)
    jobs = range(number_jobs)
    days = range(number_days)
    schedule = range(number_total_shifts)
    qualifications = range(number_qualifications)

    # 1) Creation of the model
    model = cp_model.CpModel()

    # 2) Creation of decision variables
    # newBoolVar: creates a 0-1 with the given name
    # shifts[(e, s, j)] = 1 if job j is assigned to employee e on shift s, otherwise = 0
    # similar to the xesj decision variable
    shifts = {}
    for e in employees:
        for s in schedule:
            for j in jobs:
                shifts[(e, s, j)] = model.NewBoolVar('shift_n%id%is%i' % (e, s, j))

    # 3) Creation of General Constraints

    # 3.1) General_Constraint1: each job on a shift has to be assigned to (only) exactly 1 employee e
    # for each s and j the sum of all employees must be equal to 1
    for s in schedule:
        for j in jobs:
            model.Add(sum(shifts[(e, s, j)] for e in employees) == 1)

    # 3.2) General_Constraint2: each employee works maximum on 1 job per shift
    # for each e and s the sum of all jobs must be smaller/equal to 1
    for e in employees:
        for s in schedule:
            model.Add(sum(shifts[(e, s, j)] for j in jobs) <= 1)

    # 4) Creation of Specific  Constraints

    # 4.1) Specific constraint: each employee works maximum of X shifts per week as well as a minimum of Y shifts per week
    # for each e the sum over all jobs and days must be smaller/equal to X and be larger/equal to Y

    # Counts number of shifts per employee, this sum should be smaller than the (individual) maximum working shifts per employee
    #in the same time this sum should be larger than the (individual) minimum working shifts per employee
    for e in employees:
        num_shifts_of_employee = []
        for s in schedule:
            for j in jobs:
                num_shifts_of_employee.append(shifts[(e, s, j)])
        model.Add(sum(num_shifts_of_employee) <= max_shifts_per_employee[e])
        model.Add(sum(num_shifts_of_employee) >= min_shifts_per_employee[e])

    # 4.2) Specific constraint: each employee can only be assigned to shifts when he/she is available
    for e in employees:
        for s in schedule:
            for j in jobs:
                model.Add(shifts[(e, s, j)] <= employee_availability_matrix[e, s])

    # 4.3) Specific constraint: each employee needs to have a minimum skill/qualification to accomplish a task

    # calculate array length to create an array to store "Intermediate results", based on which
    # the employee_job_calculation_matrix will be calculated
    arr_length = number_employees * number_qualifications * number_jobs
    storage = np.zeros(arr_length, dtype=int)
    counter: int = 0

    # 4.3.1) step 1: calculate employee_job_calculation_matrix
    for e in employees:
        for j in jobs:
            for q in qualifications:
                storage[counter] = calculateScore(e, q, j, employee_qualification_matrix,
                                                  job_required_qualification_matrix)

                # after each number of qualifications, a sum will be calculated of the last 3 calculatedScores in the storage array
                # if the sum = 3 (number of qualifications) -->employee has the necessary skills to absolve the job
                # thus 1 will be saved in the employee_job_calculation_matrix
                # otherwise if the sum < 3 (number of qualifications) -->employee does not have the necessary skills to absolve the job
                #because the employee does not have the required minimum qualification of at least 1 of the 3 qualifications
                if counter % number_qualifications:
                    # -1,-2,-3 depends on number of qualifications, needs to be adjusted in case of change of qualifications!!
                    if storage[counter] + storage[counter - 1] + storage[counter - 2] == number_qualifications:
                        employee_job_calculation_matrix[e, j] = 1
                    else:
                        employee_job_calculation_matrix[e, j] = 0
                counter = counter + 1

    print('employee_job_calculation_matrix:')
    print(employee_job_calculation_matrix)
    print()

    # 4.3.2) step 2: use employee_job_calculation_matrix to define constraint on solution
    # each time 0 occurs in the employee_job_calculation_matrix, the employee is not able to work on the respective job
    # attention starts counting for e and j at 0 and not at 1
    print('The employee-job restrictions are:')
    for e in employees:
        for j in jobs:
            if employee_job_calculation_matrix[e, j] == 0:
                print('employee', e, 'can not work on job', j)
                for s in schedule:
                    model.Add(shifts[(e, s, j)] == 0)
    print()

    # 4.4) Specific constraint: each employee is scheduled maximum a certain times for one task = rotation constraint
    #the sum of scheduled shifts per job per employee has to be smaller equal to the rotation preference per employee
    #thus smaller equal to the maximum of numbers of shifts per job per employee
    for e in employees:
        for j in jobs:
            model.Add(sum(shifts[(e, s, j)] for s in schedule) <= rotation_preference_per_employee[e])

    # 5.) Definition objective: minimize employee preferences
    objective = sum(shifts[(e, s, j)] * employee_job_preference_matrix[e, j] for e in employees
            for s in schedule for j in jobs)
    model.Maximize(objective)

    # 6.) Problem solver
    # Cp.Solver(): searches for solutions
    solver = cp_model.CpSolver()
    solver.Solve(model)

    # 7.) Show solution:
    # create array which saves number of shifts per employee and is increased by 1 each time value = 1
    number_shifts_per_employee = [0 for i in range(number_employees)]
    counter_day: int = 1

    # print solution: overall schedule
    for s in schedule:
        print('Day', counter_day, 'Shift', s + 1)
        counter_day = divsible(s + 1, number_shifts_per_day, counter_day)
        for e in employees:
            for j in jobs:
                if solver.Value(shifts[(e, s, j)]) == 1:
                    print('Employee', e, 'works on job', j)
                    number_shifts_per_employee[e] = number_shifts_per_employee[e] + 1
        print()

    # print number of shifts per employee
    print()
    print('Overview total number of shifts per employee:')
    for e in employees:
        print('Employee', e, 'works on', number_shifts_per_employee[e], 'shifts in total')

    # print total preference score of all employees (=the objective, which should be minimized)
    total_score: int = 0
    individual_score = [0 for i in range(number_employees)]

    for e in employees:
        for s in schedule:
            for j in jobs:
                if solver.Value(shifts[(e, s, j)]) == 1:
                    total_score = total_score + employee_job_preference_matrix[e, j]
                    individual_score[e] = individual_score[e] + employee_job_preference_matrix[e, j]

    print()
    print('The total preference score is:', total_score)
    #Alternative: to display total preference:
    #print(solver.ObjectiveValue())


    # print individual preference score per employee
    print()
    print('Total individual preference score per employee:')
    for e in employees:
        print('Employee ', e, 'has a preference score of: ', individual_score[e])

    # print total average preference score per employee:
    total_average_preference_score = total_score / number_employees
    print('Total average preference score per employee:' , total_average_preference_score)

    #print individual average preference score per employee
    #round function rounds to x decimal places
    print()
    print('Individual average preference score per employee:')
    for e in employees:
        print('Employee ', e, 'has an average preference score of: ', round(individual_score[e] / number_shifts_per_employee[e],2))

    #print maximum (possible) preference score per employee
    print()

    #array maxInRows saves the maximum (possible) preference score for each employee
    #in the employee_job_preference_matrix
    maxInRows = np.amax(employee_job_preference_matrix, axis = 1)

    print('Maximum preference score per employee:')
    for e in employees:
        print('Employee ', e, 'has a maximum possible preference score of: ', maxInRows[e])

    # Code to determine if an optimal solutions could be found
    status = solver.Solve(model)

    print()
    print('The status is:', status)

    # optimality of solution:
    if status == cp_model.OPTIMAL:
        print('Optimal solution found')
    elif status == cp_model.FEASIBLE:
        print('A solutions found, but may not be optimal')
    else:
        print('No solution could be found')

    # print solution: individual schedule for each employee
    print()
    print('Individual schedule per employee:')

    #counter_day resets counter day to 1 at the beginning and for each employee
    # (counter day to transform shifts into days)
    for e in employees:
        print('Employee', e, 'has the following schedule:')
        counter_day = 1
        for s in schedule:
            for j in jobs:
                if solver.Value(shifts[(e, s, j)]) == 1:
                    print('day', counter_day,'in shift', s+1, 'on job',j )
            counter_day = divsible(s + 1, number_shifts_per_day, counter_day)

        print()

    # method to check if number is divisible by shift per day -->if yes, increase counter_day by 1 to jump to next day

    #stop time and print out the time taken to calculate a solution
    time_end = time.time()
    print(f"Runtime of the program is {time_end - time_start} seconds")

def divsible(currentschedule, numbershifts, counter_day):
    if currentschedule % numbershifts == 0:
        counter_day = counter_day + 1
    return counter_day

    # method that calculates if an employee has the required level of qualification for a job

def calculateScore(employee, qualification, job, employee_qualification_matrix, job_required_qualification_matrix):
    if employee_qualification_matrix[employee, qualification] > job_required_qualification_matrix[job, qualification]:
        return 0
    return 1

if __name__ == '__main__':
    main()
