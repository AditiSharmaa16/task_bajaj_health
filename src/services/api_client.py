import requests
from src.config import Config
from src.utils.logger import log

class APIClient:
    @staticmethod
    def generate_webhook():
        url = f"{Config.BASE_URL}/generateWebhook/PYTHON"
        payload = {
            "name": Config.NAME,
            "regNo": Config.REG_NO,
            "email": Config.EMAIL
        }
        
        try:
            log.info("Generating webhook...")
            response = requests.post(
                url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Failed to generate webhook: {str(e)}")
            return None

    @staticmethod
    def submit_solution(webhook_url, access_token, sql_query):
        try:
            log.info("Submitting solution...")
            response = requests.post(
                webhook_url,
                json={"finalQuery": sql_query},
                headers={
                    'Authorization': access_token,
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Failed to submit solution: {str(e)}")
            return None