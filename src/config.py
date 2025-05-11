import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv('BASE_URL')
    NAME = os.getenv('NAME')
    REG_NO = os.getenv('REG_NO')
    EMAIL = os.getenv('EMAIL')
    
    @classmethod
    def get_question_url(cls):
        last_digit = int(cls.REG_NO[-1]) if cls.REG_NO and cls.REG_NO[-1].isdigit() else 0
        return (
            "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing"
            if last_digit % 2 != 0 
            else "https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view?usp=sharing"
        )