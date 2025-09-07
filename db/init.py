import sqlite3
from pathlib import Path

DB_PATH = Path("data/financial_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database_from_sql():
    base_dir = Path(__file__).resolve().parent.parent  # 找到项目根目录
    schema_path = base_dir / "db" / "scripts" / "schema.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()


 