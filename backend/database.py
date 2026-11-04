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
        latitude REAL,      -- 위도 컬럼 추가
        longitude REAL,     -- 경도 컬럼 추가
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 테이블이 생성되어 있는 경우를 대비해 컬럼 추가 (ALTER TABLE)
    try:
        cursor.execute("ALTER TABLE real_estate_deals ADD COLUMN latitude REAL")
        cursor.execute("ALTER TABLE real_estate_deals ADD COLUMN longitude REAL")
    except sqlite3.OperationalError:
        pass    # 컬럼이 존재하면 넘어가기

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
            d["deal_day"],
            d.get("latitude"),      # 좌표가 있으면 넣고 없으면 None
            d.get("longitude")      # 좌표가 있으면 넣고 없으면 None
        ) for d in deals
    ]
    
    cursor.executemany(insert_sql, data_tuples)
    conn.commit()
    inserted_count = cursor.rowcount
    conn.close()
    
    return inserted_count

if __name__ == "__main__":
    init_db()