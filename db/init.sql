CREATE DATABASE IF NOT EXISTS main_db;
USE main_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- ユーザ-アカウント用のテーブル
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- スタンプ用のテーブル
CREATE TABLE IF NOT EXISTS stamps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(255) NOT NULL,
    qr_code VARCHAR(255) NOT NULL
);

ALTER TABLE stamps ADD COLUMN is_peak BOOLEAN DEFAULT FALSE;

INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A2', TRUE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B2', TRUE);


-- 特典用のテーブル
CREATE TABLE IF NOT EXISTS gifts (
    id INT AUTO_DECREMENT PRIMATY KEY,
    store_name VARCHAR(255) NOT NULL,
    item_id INT NOT NULL
)

ALTER TABLE gifts ADD FOREIGN KEY (item_id) REFERENCES items(id);

INSERT INTO items (name, description) VALUES ('蕎麦屋', '蕎麦10％引き');
INSERT INTO items (name, description) VALUES ('団子屋', 'みたらし団子1個無料');
INSERT INTO items (name, description) VALUES ('銭湯', 'レンタルタオル無料');