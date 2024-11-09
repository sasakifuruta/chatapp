-- コンテナ初回起動時に実行するSQL
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

-- ユーザテーブル
CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,             -- ユーザID　uid
    user_name varchar(255) UNIQUE NOT NULL,   -- ユーザ名
    email varchar(255) UNIQUE NOT NULL,       -- メールアドレス
    password varchar(255) NOT NULL,           -- パスワード
    is_active BOOLEAN NOT NULL DEFAULT TRUE,  -- 退会していないなら、TRUE（１）
    profile_url text,                         -- プロフィール画像url
    -- barth_date date NOT NULL               -- 学年を判別するための生年月日
);

-- お母さん画像スケジュールテーブル
-- CREATE TABLE mom_schedules (
    -- id
    -- barth_date date REFERENCES users(barth_date)  -- 生年月日
    -- start_time datetime NOT NULL
    -- end_time datetime NOT NULL
-- );

-- チャットグループテーブル
CREATE TABLE groups (
    id serial PRIMARY KEY,                            -- グループID gid
    uid varchar(255) REFERENCES users(uid),           -- グループ作成ユーザID
    name varchar(255) UNIQUE NOT NULL,                -- グループ名
    img_url text                                      -- グループ画像
);

-- メッセージテーブル
CREATE TABLE messages (
    id serial PRIMARY KEY,                               -- メッセージID mid
    uid varchar(255) REFERENCES users(uid),              -- 送信者uid
    gid integer REFERENCES groups(id) ON DELETE CASCADE, --　グループID
    content text,                                        -- メッセージ内容
    send_at timestamp not null default current_timestamp,  --　送信時間
);

-- メッセージステータステーブル
CREATE TABLE message_status (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),                  -- 受信者uid
    mid integer REFERENCES messages(id) ON DELETE CASCADE,   -- メッセージID
    is_read BOOLEAN NOT NULL DEFAULT FALSE,                  -- 既読ならTRUE（１）
    
);

INSERT INTO users(uid, user_name, email, password)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO groups(id, uid, name)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','テスト用');
INSERT INTO messages(id, uid, gid, content)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')
INSERT INTO message_status(id, uid, mid)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1')


