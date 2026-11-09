import os
import sqlite3
import requests
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드 (.env 위치에 맞게 설정)
load_dotenv()
# backend/.env 에 있는 경우: load_dotenv(dotenv_path='backend/.env')

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

def get_coordinates(address):
    """
    주소 문자열을 받아 카카오 Local API를 통해 (위도, 경도) 튜플을 반환합니다.
    """
    if not KAKAO_REST_API_KEY:
        print("Error: KAKAO_REST_API_KEY가 설정되지 않았습니다.")
        return None, None

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }
    params = {
        "query": address
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents")
            
            if documents:
                # 첫 번째 검색 결과의 경도(x), 위도(y) 추출
                longitude = float(documents[0]["x"])
                latitude = float(documents[0]["y"])
                return latitude, longitude
            else:
                print(f"주소 검색 결과 없음: {address}")
                return None, None
        else:
            print(f"API 요청 실패 (Status Code: {response.status_code}): {response.text}")
            return None, None

    except Exception as e:
        print(f"지오코딩 처리 중 오류 발생: {e}")
        return None, None

def update_db_coordinates(db_path = "rhc_database.db"):
    if not os.path.exists(db_path) and os.path.exists("backend/rhc_database.db"):
        db_path = "backend/rhc_database.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 좌표가 없는 데이터 조회
    cursor.execute(""" 
        SELECT id, building_name
        From real_estate_deals
        WHERE latitude IS NULL OR longitude IS NULL 
    """)
    rows = cursor.fetchall()

    if not rows:
        print("모든 데이터의 좌표 업데이트가 이미 완료되어 있습니다.")
        conn.close()
        return

    print(f"총 {len(rows)}건의 좌표 미등록 데이터 발견, 변활을 시작합니다...")

    for row_id, building_name in rows:
        # TODO: 추후 전국 데이터 확장 시 '서울특별시 종로구' 하드코딩 제거
        # -> DB의 시/도, 군/구, 동 (city, district, dong)을 함께 조회해서 f"{city} {district} {dong} {building_name}" 동적조합으로 수정
        search_query = f"서울특별시 종로구 {building_name}"
        lat, lng = get_coordinates(search_query)

        if lat and lng:
            cursor.execute("""
                UPDATE real_estate_deals
                SET latitude = ?, longitude = ?
                WHERE id = ?
            """, (lat, lng, row_id))
            print(f"[성공] {building_name} -> Lat: {lat}, Lng: {lng}")
        else:
            print(f"[실패] 좌표 변환 불가 : {building_name}")

    conn.commit()
    conn.close()
    print("DB 좌표 업데이트 완료")
    
if __name__ == "__main__":
    update_db_coordinates()