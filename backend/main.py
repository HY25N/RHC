# main.py
from database import init_db, save_deals
from molit_parser import fetch_real_estate_data
from kakao_geocoder import update_db_coordinates

def run_pipeline():
    print("=== [Phase 1] 국토부 API 데이터 수집 및 DB 저장 시작 ===")
    init_db()
    
    deals = fetch_real_estate_data()
    if deals:
        saved_count = save_deals(deals)
        print(f"DB 저장 완료: 총 {saved_count}건 적재됨")
    else:
        print("수집된 데이터가 없습니다.")
    
    print("\n=== [Phase 2] DB 미등록 데이터 카카오 지오코딩 좌표 변환 시작 ===")
    update_db_coordinates()
    
    print("\n=== 전체 파이프라인 프로세스 완료 ===")

if __name__ == "__main__":
    run_pipeline()