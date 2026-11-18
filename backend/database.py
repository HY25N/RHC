import sqlite3

def init_db():
    """DB 연결 및 테이블 생성"""
    conn = sqlite3.connect("rhc_database.db")
    cursor = conn.cursor()
    
    # dong, jibun, floor 컬럼 추가 + UNIQUE 제약으로 중복 거래 방지
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS real_estate_deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_code TEXT NOT NULL,
        dong TEXT NOT NULL DEFAULT '',
        jibun TEXT NOT NULL DEFAULT '',
        building_name TEXT NOT NULL,
        deal_type TEXT NOT NULL,
        deposit INTEGER NOT NULL,
        monthly_rent INTEGER NOT NULL DEFAULT 0,
        exclusive_area REAL NOT NULL DEFAULT 0,
        deal_year INTEGER NOT NULL,
        deal_month INTEGER NOT NULL,
        deal_day INTEGER NOT NULL DEFAULT 0,
        floor TEXT NOT NULL DEFAULT '',
        latitude REAL,
        longitude REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(region_code, dong, building_name, deal_type, deposit, monthly_rent,
               exclusive_area, deal_year, deal_month, deal_day, floor)
    )
    """)

    conn.commit()
    conn.close()

def save_deals(deals):
    """파싱된 거래 데이터를 DB에 삽입(중복은 무시)하고, 신규 삽입 건수를 반환"""
    conn = sqlite3.connect("rhc_database.db")
    cursor = conn.cursor()

    # INSERT OR IGNORE: UNIQUE에 걸리는 중복 거래는 에러 없이 건너뜀
    insert_sql = """
    INSERT OR IGNORE INTO real_estate_deals
    (region_code, dong, jibun, building_name, deal_type, deposit, monthly_rent,
     exclusive_area, deal_year, deal_month, deal_day, floor)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # ? 12개와 값 12개의 개수가 같아야 함 (좌표는 지오코더가 나중에 UPDATE로 채움)
    data_tuples = [
        (
            d["region_code"],
            d["dong"],
            d.get("jibun", ""),  # parser가 jibun을 안 주면 빈 값
            d["building_name"],
            d["deal_type"],
            d["deposit"],
            d["monthly_rent"],
            d["exclusive_area"],
            d["deal_year"],
            d["deal_month"],
            d["deal_day"],
            d["floor"]
        ) for d in deals
    ]
    
    cursor.executemany(insert_sql, data_tuples)
    conn.commit()

    # 새 연결에서의 total_changes = 이번에 실제로 삽입된 건수 (무시된 중복은 제외)
    inserted_count = conn.total_changes
    conn.close()
    
    return inserted_count

if __name__ == "__main__":
    init_db()