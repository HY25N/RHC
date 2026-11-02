import sqlite3

def init_db():
    """DB 연결 및 테이블 생성 (schema.sql 기반)"""
    conn = sqlite3.connect("rhc_database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS real_estate_deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_code TEXT NOT NULL,
        building_name TEXT NOT NULL,
        deal_type TEXT NOT NULL,
        deposit INTEGER NOT NULL,
        monthly_rent INTEGER DEFAULT 0,
        exclusive_area REAL,
        deal_year INTEGER NOT NULL,
        deal_month INTEGER NOT NULL,
        deal_day INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_deals(deals):
    """파싱된 거래 데이터를 DB에 삽입"""
    conn = sqlite3.connect("rhc_database.db")
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO real_estate_deals 
    (region_code, building_name, deal_type, deposit, monthly_rent, exclusive_area, deal_year, deal_month, deal_day)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    data_tuples = [
        (
            d["region_code"],
            d["building_name"],
            d["deal_type"],
            d["deposit"],
            d["monthly_rent"],
            d["exclusive_area"],
            d["deal_year"],
            d["deal_month"],
            d["deal_day"]
        ) for d in deals
    ]
    
    cursor.executemany(insert_sql, data_tuples)
    conn.commit()
    inserted_count = cursor.rowcount
    conn.close()
    
    return inserted_count