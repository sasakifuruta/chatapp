import pymysql
from flask import abort
from util.DB import DB


class dbConnect:
    
    
    # 新規登録
    @staticmethod
    def createUser(uid, name, email, password):
        try:
            print('nao')
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (uid, name, email, password))
            # cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


            
    
    # アクティブなユーザを取得
    @staticmethod
    def getUser(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email = %s AND is_active = 1;"
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()

    
    
    # # アカウント・プロフィール画像編集
    # @staticmethod
    # def updateUser(name, email, password, profile_url, uid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "UPDATE users SET name=%s, email=%s, password=%s, profile_url=%s WHERE uid=%s;"
    #         cur.execute(sql, (name, email, password, profile_url, uid))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()

    

    # # 退会処理
    # @staticmethod
    # def deactivateUser(uid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "UPDATE users SET is_active = 0 WHERE uid=%s;"
    #         cur.execute(sql, (uid,))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()



    # # 全グループを取得
    # @staticmethod
    # def getGroupAll():
    #         try:
    #             conn = DB.getConnection()
    #             cur = conn.cursor()
    #             sql = "SELECT * FROM groups;"
    #             cur.execute(sql)
    #             groups = cur.fetchall()
    #             return groups
    #         except Exception as e:
    #             print(f'エラーが発生しています: {e}')
    #             abort(500)
    #         finally:
    #             cur.close()

            
    
    # @staticmethod
    # def getGroupById(gid):
    #         try:
    #             conn = DB.getConnection()
    #             cur = conn.cursor()
    #             sql = "SELECT * FROM groups WHERE id=%s;"
    #             cur.execute(sql, (gid,))
    #             group = cur.fetchone()
    #             return group
    #         except Exception as e:
    #             print(f'エラーが発生しています: {e}')
    #             abort(500)
    #         finally:
    #             cur.close()

    
    
    # @staticmethod
    # def getGroupByName(group_name):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "SELECT * FROM groups WHERE name=%s;"
    #         cur.execute(sql, (group_name,))
    #         group = cur.fetchone()
    #         return group
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()

            
    
    # # グループ追加
    # @staticmethod
    # def addGroup(uid, newGroupName, newGroup_img):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "INSERT INTO groups (uid, name, img_url) VALUES (%s, %s, %s);"
    #         cur.execute(sql, (uid, newGroupName, newGroup_img))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    
    # # グループ編集
    # @staticmethod
    # def updateGroup(uid, newGroupName, newGroup_img, gid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "UPDATE groups SET uid=%s, name=%s, img_url=%s WHERE id=%s;"
    #         cur.execute(sql, (uid, newGroupName, newGroup_img, gid))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    
    # # グループ削除
    # @staticmethod
    # def deleteGroup(gid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "DELETE FROM groups WHERE id=%s;"
    #         cur.execute(sql, (gid,))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    
    # # メッセージを取得
    # @staticmethod
    # def getMessageAll(gid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "SELECT id,u.uid, user_name, content FROM messages AS m INNER JOIN users As u ON m.uid=u.uid WHERE gid=%s;"
    #         cur.execute(sql, (gid,))
    #         messages = cur.fetchall()
    #         return messages
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    
    # # メッセージ追加
    # @staticmethod
    # def createMessage(uid, gid, content):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "INSERT INTO messages(uid, gid, content) VALUES(%s,%s,%s);"
    #         cur.execute(sql, (uid, gid, content))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    
    # # メッセージ更新
    # @staticmethod
    # def updateMessage(content, mid):
    #         try:
    #             conn = DB.getConnection()
    #             cur = conn.cursor()
    #             sql = "UPDATE messages SET content=%s WHERE mid=%s;"
    #             cur.execute(sql, (content, mid))
    #             conn.commit()
    #         except Exception as e:
    #             print(f'エラーが発生しています: {e}')
    #             abort(500)
    #         finally:
    #             cur.close()


    
    # # メッセージ削除
    # @staticmethod
    # def deleteMessage(mid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "DELETE FROM messages WHERE mid=%s;"
    #         cur.execute(sql, (mid,))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています: {e}')
    #         abort(500)
    #     finally:
    #         cur.close()
