
DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';


CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY,             
    user_name VARCHAR(255) UNIQUE NOT NULL,   
    email VARCHAR(255) UNIQUE NOT NULL,       
    password VARCHAR(255) NOT NULL,           
    is_active BOOLEAN NOT NULL DEFAULT TRUE,  
    profile_img TEXT                          
);


CREATE TABLE chat_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,                            
    uid VARCHAR(255) REFERENCES users(uid),           
    name VARCHAR(255) UNIQUE NOT NULL,                
    group_img TEXT                               
);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,                                 
    uid VARCHAR(255) REFERENCES users(uid),                
    cid INTEGER REFERENCES chat_groups(id) ON DELETE CASCADE,   
    content TEXT,                                          
    send_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  
);

INSERT INTO users(uid, user_name, email, password, is_active, profile_img)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テストですよ','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', 1, 'http://yahoo.co.jp/img.png');
INSERT INTO chat_groups(id, uid, name, group_img)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','テスト用', 'http://yahoo.co.jp/img.png');
INSERT INTO messages(id, uid, cid, content, send_at)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', 1, '誰かかまってください、、', '2024-11-10 23:30:00')


