import sqlite3
from pathlib import Path

from fastapi import FastAPI, Query

app = FastAPI(title="RHC API")

# DB 파일은 api.py와 같은 폴더(backend)의 것을 사용 (실행 위치와 무관)
DB_PATH = Path(__file__).resolve().parent / "rhc_database.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 결과를 컬럼 이름으로 꺼낼 수 있게 함
    return conn


@app.get("/health")
def health():
    """서버가 살아 있는지 확인하는 가장 작은 엔드포인트"""
    return {"status": "ok"}


@app.get("/buildings")
def search_buildings(q: str = Query(..., min_length=1, description="건물명 검색어")):
    """건물명에 검색어가 포함된 건물 목록 (건물 단위로 묶어서 반환)"""
    sql = """
        SELECT region_code, dong, jibun, building_name,
               MAX(latitude)  AS latitude,
               MAX(longitude) AS longitude,
               COUNT(*)       AS deal_count
        FROM real_estate_deals
        WHERE building_name LIKE ?
        GROUP BY region_code, dong, jibun, building_name
        ORDER BY building_name, dong
        LIMIT 50
    """
    conn = get_connection()
    try:
        rows = conn.execute(sql, (f"%{q}%",)).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]