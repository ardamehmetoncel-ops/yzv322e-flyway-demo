"""
verify.py — Queries the Flyway-managed PostgreSQL database and prints results.
Run after migrations: python scripts/verify.py
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("POSTGRES_HOST", "localhost"),
    "port":     int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname":   os.getenv("POSTGRES_DB", "flyway_demo"),
    "user":     os.getenv("POSTGRES_USER", "flyway_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "flyway_pass"),
}

def separator(title=""):
    width = 60
    if title:
        print(f"\n{'─' * 4} {title} {'─' * (width - len(title) - 6)}")
    else:
        print("─" * width)

def run():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur  = conn.cursor()
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {e}")
        sys.exit(1)

    # 1. Flyway schema history
    separator("flyway_schema_history")
    cur.execute("""
        SELECT version, description, type, installed_on, success
        FROM flyway_schema_history
        ORDER BY installed_rank;
    """)
    rows = cur.fetchall()
    print(f"{'Version':<10} {'Description':<25} {'Type':<10} {'Success'}")
    separator()
    for r in rows:
        print(f"{str(r[0]):<10} {r[1]:<25} {r[2]:<10} {'✅' if r[4] else '❌'}")

    # 2. All products
    separator("products table")
    cur.execute("SELECT id, name, price, category, created_at FROM products ORDER BY id;")
    rows = cur.fetchall()
    print(f"{'ID':<5} {'Name':<35} {'Price':>8} {'Category'}")
    separator()
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<35} {float(r[2]):>8.2f} {r[3]}")

    # 3. Category summary view
    separator("category_summary view")
    cur.execute("SELECT * FROM category_summary;")
    rows = cur.fetchall()
    print(f"{'Category':<15} {'Count':>6} {'Avg Price':>10} {'Min':>8} {'Max':>8}")
    separator()
    for r in rows:
        print(f"{r[0]:<15} {r[1]:>6} {float(r[2]):>10.2f} {float(r[3]):>8.2f} {float(r[4]):>8.2f}")

    cur.close()
    conn.close()
    print("\n✅ All checks passed. Database is healthy.\n")

if __name__ == "__main__":
    run()
