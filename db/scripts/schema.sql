CREATE TABLE IF NOT EXISTS usage_log (
            user_id TEXT,
            used_on DATE,
            count INTEGER,
            PRIMARY KEY (user_id, used_on)
);

CREATE TABLE IF NOT EXISTS invoice_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    file_name TEXT,
    image_path TEXT,
    invoice_date TEXT,
    issuer TEXT,
    total_amount REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    description TEXT,
    category TEXT,
    amount REAL,
    FOREIGN KEY(invoice_id) REFERENCES invoice_records(id)
);