from datetime import datetime
from src.config import Config
from src.utils.logger import log

class SQLSolver:
    @staticmethod
    def calculate_age(dob):
        today = datetime.today()
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    @staticmethod
    def solve_problem():
        question_url = Config.get_question_url()
        log.info(f"Solving SQL problem from: {question_url}")
        
        if "1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY" in question_url:
            return """
            WITH filtered_payments AS (
                SELECT 
                    p.EMP_ID,
                    p.AMOUNT AS SALARY,
                    DAY(p.PAYMENT_TIME) AS payment_day
                FROM PAYMENTS p
                WHERE DAY(p.PAYMENT_TIME) != 1  -- Exclude 1st day of month
            ),
            max_salary AS (
                SELECT MAX(SALARY) AS max_salary
                FROM filtered_payments
            )
            SELECT 
                fp.SALARY,
                CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
                FLOOR(DATEDIFF(CURRENT_DATE, e.DOB)/365) AS AGE,
                d.DEPARTMENT_NAME
            FROM filtered_payments fp
            JOIN EMPLOYEE e ON fp.EMP_ID = e.EMP_ID
            JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
            JOIN max_salary ms ON fp.SALARY = ms.max_salary
            LIMIT 1;
            """
        else:
            return """
            WITH employee_ages AS (
                SELECT 
                    e.EMP_ID,
                    e.FIRST_NAME,
                    e.LAST_NAME,
                    e.DEPARTMENT,
                    FLOOR(DATEDIFF(CURRENT_DATE, e.DOB)/365) AS AGE,
                    d.DEPARTMENT_NAME
                FROM EMPLOYEE e
                JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
            )
            SELECT 
                e1.EMP_ID,
                e1.FIRST_NAME,
                e1.LAST_NAME,
                e1.DEPARTMENT_NAME,
                COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
            FROM employee_ages e1
            LEFT JOIN employee_ages e2 ON 
                e1.DEPARTMENT = e2.DEPARTMENT AND
                e2.AGE < e1.AGE AND
                e2.EMP_ID != e1.EMP_ID
            GROUP BY 
                e1.EMP_ID,
                e1.FIRST_NAME,
                e1.LAST_NAME,
                e1.DEPARTMENT_NAME
            ORDER BY e1.EMP_ID DESC;
            """