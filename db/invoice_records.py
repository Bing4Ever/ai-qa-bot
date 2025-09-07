import json
import os
from datetime import datetime
from db.init import get_connection

def save_invoice_record(user_id: str, file_path: str, file_name: str, json_data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO invoice_records (
            user_id, file_name, image_path, invoice_date, issuer, total_amount
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        file_name,
        file_path,
        json_data.get("invoice_date"),
        json_data.get("issuer"),
        float(json_data.get("total_amount", 0))
    ))

    invoice_id = cursor.lastrowid

    items = json_data.get("items", [])
    for item in items:
        cursor.execute('''
            INSERT INTO invoice_items (invoice_id, description, category, amount)
            VALUES (?, ?, ?, ?)
        ''', (
            invoice_id,
            item.get("description"),
            item.get("category"),
            float(item.get("amount", 0))
        ))

    conn.commit()
    conn.close()

def get_invoice_records_by_user(user_id: str, page: int = 1, page_size: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size
    cursor.execute("""
        SELECT id, file_name, image_path, invoice_date, issuer, total_amount, created_at
        FROM invoice_records
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, (user_id, page_size, offset))

    records = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM invoice_records WHERE user_id = ?
    """, (user_id,))
    total_count = cursor.fetchone()[0]

    conn.close()

    return records, total_count