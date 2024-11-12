import pymysql
import pymysql.cursors

class DB:
    def getConnection():
        try:
            conn = pymysql.connect(
                host = "db",  #RDS接続時にはdbをRDSアドレスに変更する
                db = "chatapp",
                user = "testuser",
                password = "testuser",
                charset = "utf8",
                cursorclass = pymysql.cursors.DictCursor
            )
            return conn
        except(ConnectionError):
            print("コネクションエラーです")
            conn.close()