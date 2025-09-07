import sqlite3
from datetime import datetime
from db.init import get_connection

def check_quota(user_id: str, daily_limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.today().date()    

    # 读取今天的记录
    cursor.execute("SELECT count FROM usage_log WHERE user_id=? AND used_on=?", (user_id, today))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO usage_log (user_id, used_on, count) VALUES (?, ?, 0)", (user_id, today))
        conn.commit()
        return True
    else:
        if row[0] >= daily_limit:
            return False
        else:
            return True

def add_usage(user_id: str):
    conn = get_connection()
    today = datetime.today().date()
    cursor = conn.cursor()
    cursor.execute("UPDATE usage_log SET count = count + 1 WHERE user_id=? AND used_on=?", (user_id, today))
    conn.commit()

def get_remaining_quota(user_id, daily_limit):
    conn = get_connection()
    today = datetime.today().date()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM usage_log WHERE user_id=? AND used_on=?", (user_id, today))
    row = cursor.fetchone()
    return daily_limit - (row[0] if row else 0)