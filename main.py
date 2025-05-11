import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.services.api_client import APIClient
from src.services.sql_solver import SQLSolver
from src.utils.logger import log

def main():
    log.info("Starting SQL Webhook Solver Application")
    
    webhook_response = APIClient.generate_webhook()
    if not webhook_response:
        log.error("Application failed - could not generate webhook")
        return
    
    webhook_url = webhook_response.get('webhook')
    access_token = webhook_response.get('accessToken')
    
    if not webhook_url or not access_token:
        log.error("Invalid webhook response - missing required fields")
        return
    
    log.info(f"Webhook URL received: {webhook_url}")
    
    sql_solution = SQLSolver.solve_problem()
    log.info(f"Generated SQL solution:\n{sql_solution}")
    
    submission_response = APIClient.submit_solution(
        webhook_url=webhook_url,
        access_token=access_token,
        sql_query=sql_solution
    )
    
    if submission_response:
        log.info("Solution submitted successfully!")
        log.info(f"Response: {submission_response}")
    else:
        log.error("Failed to submit solution")

if __name__ == "__main__":
    main()