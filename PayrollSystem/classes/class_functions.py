from datetime import datetime

def check_date(date):
    try:
        datetime.strptime(date, "%Y-%m")
        return True
    except Exception:
        return False
