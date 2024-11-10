-- コンテナ初回起動時に実行するSQL
DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

-- ユーザテーブル
CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY,             -- ユーザID　uid
    user_name VARCHAR(255) UNIQUE NOT NULL,   -- ユーザ名
    email VARCHAR(255) UNIQUE NOT NULL,       -- メールアドレス
    password VARCHAR(255) NOT NULL,           -- パスワード
    is_active BOOLEAN NOT NULL DEFAULT TRUE,  -- アクティブなら、TRUE（１）
    profile_img TEXT                          -- プロフィール画像url
);

-- チャットグループテーブル
CREATE TABLE chat_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,                            -- グループID gid
    uid VARCHAR(255) REFERENCES users(uid),           -- グループ作成ユーザID
    name VARCHAR(255) UNIQUE NOT NULL,                -- グループ名
    chat_group_img TEXT                               -- グループ画像
);

-- メッセージテーブル
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,                                 -- メッセージID mid
    uid VARCHAR(255) REFERENCES users(uid),                -- 送信者uid
    cid INTEGER REFERENCES chat_groups(id) ON DELETE CASCADE,   --　チャットグループID
    content TEXT,                                          -- メッセージ内容
    send_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  --　送信時間
);

INSERT INTO users(uid, user_name, email, password)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO groups(id, uid, name)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','テスト用');
INSERT INTO messages(id, uid, gid, content)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')


