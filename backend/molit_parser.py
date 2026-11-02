import requests
import xml.etree.ElementTree as ET
from database import init_db, save_deals

def parse_real_estate_xml(xml_data):
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    
    parsed_list = []
    for item in items:
        deposit_str = item.findtext("deposit", "0").strip().replace(",", "")
        monthly_rent_str = item.findtext("monthlyRent", "0").strip().replace(",", "")
        
        area_str = item.findtext("excluUseAr", "0").strip()
        
        deal_info = {
            "building_name": item.findtext("aptNm", "").strip(),
            "region_code": item.findtext("sggCd", "").strip(),
            "dong": item.findtext("umdNm", "").strip(),
            "deposit": int(deposit_str) if deposit_str.isdigit() else 0,
            "monthly_rent": int(monthly_rent_str) if monthly_rent_str.isdigit() else 0,
            "exclusive_area": float(area_str) if area_str else 0.0,
            "deal_year": int(item.findtext("dealYear", "0")),
            "deal_month": int(item.findtext("dealMonth", "0")),
            "deal_day": int(item.findtext("dealDay", "0")),
            "floor": item.findtext("floor", "").strip()
        }
        
        deal_info["deal_type"] = "월세" if deal_info["monthly_rent"] > 0 else "전세"
        parsed_list.append(deal_info)
        
    return parsed_list

def fetch_real_estate_data():
    api_key = "a4f3a73ac43f647fef865da6213f51e91d7ccdb631a8ce07e04a258d3e2cadb8"
    base_url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent"
    lawd_cd = "11110"   # 종로구
    deal_ymd = "202312" # 2023년 12월
    
    url = f"{base_url}?serviceKey={api_key}&LAWD_CD={lawd_cd}&DEAL_YMD={deal_ymd}"

    print("국토부 API 데이터 수집 및 파싱 시작...")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            parsed_data = parse_real_estate_xml(response.text)
            print(f"✅ 총 {len(parsed_data)}건의 거래 데이터를 성공적으로 파싱했습니다.\n")
            
            for i, data in enumerate(parsed_data[:3], 1):
                print(f"[{i}] {data['building_name']} ({data['dong']})")
                print(f"    - 구분: {data['deal_type']} (보증금: {data['deposit']}만원 / 월세: {data['monthly_rent']}만원)")
                print(f"    - 면적: {data['exclusive_area']}㎡ ({data['floor']}층)")
                print(f"    - 계약일: {data['deal_year']}-{data['deal_month']}-{data['deal_day']}\n")
            
            return parsed_data
        else:
            print(f"❌ API 호출 실패 (상태 코드: {response.status_code})")
            return []
            
    except Exception as e:
        print(f"❌ 데이터 파싱 에러: {e}")
        return []

if __name__ == "__main__":
    init_db()  # DB 및 테이블 초기화
    deals = fetch_real_estate_data()
    
    if deals:
        saved_count = save_deals(deals)
        print(f"💾 DB 저장 완료: 총 {saved_count}건이 rhc_database.db에 적재되었습니다.")