import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute('DROP TABLE IF EXISTS employees')
    cur.execute('CREATE TABLE IF NOT EXISTS employees (employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, hire_date DATE, job_id INTEGER, salary INTEGER)')
    conn.commit()

# ADD EMPLOYEE'S INFORMATION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    fileJson = json.loads(file_data)
    for employee in fileJson:
        employee_id = employee["employee_id"]
        first_name = employee["first_name"]
        last_name = employee["last_name"]
        hire_date = employee["hire_date"]
        job_id = employee["job_id"]
        salary = employee["salary"]
        cur.execute('INSERT OR IGNORE INTO employees (employee_id, first_name, last_name, hire_date, job_id, salary) VALUES (?, ?, ?, ?, ?, ?)', (employee_id, first_name, last_name, hire_date, job_id, salary))
    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute('SELECT jobs.job_title, employees.hire_date FROM employees INNER JOIN jobs on employees.job_id = jobs.job_id ORDER BY employees.hire_date')
    job_and_date = cur.fetchall()
    return job_and_date[0][0]

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute('SELECT employees.first_name, employees.last_name FROM employees INNER JOIN jobs ON employees.job_id = jobs.job_id WHERE employees.salary < jobs.min_salary OR employees.salary > jobs.max_salary')
    names = cur.fetchall()
    return names

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    cur.execute("SELECT job_title FROM jobs ORDER BY job_id")
    x = cur.fetchall()
    for i in range(len(x)):
        x[i] = x[i][0]
    cur.execute("SELECT max_salary FROM jobs ORDER BY job_id")
    max_salary = cur.fetchall()
    for i in range(len(max_salary)):
        max_salary[i] = max_salary[i][0]
    cur.execute("SELECT min_salary FROM jobs ORDER BY job_id")
    min_salary = cur.fetchall()
    for i in range(len(min_salary)):
        min_salary[i] = min_salary[i][0]
    salaries = cur.fetchall()
    print(salaries)
    plt.scatter(x, salaries)
    plt.scatter(x, max_salary, c='r', marker='x')
    plt.scatter(x, min_salary, c='r', marker='x')
    plt.xticks(rotation=45, ha='right')
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

