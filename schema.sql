CREATE TABLE real_estate_deals (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    region_code VARCHAR(10) NOT NULL,
    building_name VARCHAR(100) NOT NULL,
    deal_type VARCHAR(10) NOT NULL,
    deposit INT NOT NULL,
    monthly_rent INT DEFAULT 0,
    exclusive_area FLOAT,
    deal_year INT NOT NULL,
    deal_month INT NOT NULL,
    deal_day INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);