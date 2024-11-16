import pymysql
from flask import abort
from util.DB import DB


class dbConnect:
    
    
    # 新規登録
    @staticmethod
    def createUser(uid, name, email, password):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (uid, name, email, password))
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
            conn.close()

    
    
    # アカウント・プロフィール画像編集
    @staticmethod
    def updateUser(name, email, password, profile_img, uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET name=%s, email=%s, password=%s, profile_img=%s WHERE uid=%s;"
            cur.execute(sql, (name, email, password, profile_img, uid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()
    

    # 退会処理
    @staticmethod
    def deactivateUser(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET is_active = 0 WHERE uid=%s;"
            cur.execute(sql, (uid,))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()



    # 全グループを取得
    @staticmethod
    def getGroupAll():
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "SELECT * FROM chat_groups;"
                cur.execute(sql)
                groups = cur.fetchall()
                return groups
            except Exception as e:
                print(f'エラーが発生しています: {e}')
                abort(500)
            finally:
                cur.close()
                conn.close()

            
    
    @staticmethod
    def getGroupById(gid):
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "SELECT * FROM chat_groups WHERE id=%s;"
                cur.execute(sql, (gid,))
                group = cur.fetchone()
                return group
            except Exception as e:
                print(f'エラーが発生しています: {e}')
                abort(500)
            finally:
                cur.close()
                conn.close()

    
    
    @staticmethod
    def getGroupByName(group_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM chat_groups WHERE name=%s;"
            cur.execute(sql, (group_name,))
            group = cur.fetchone()
            return group
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()

            
    
    # グループ追加
    @staticmethod
    def addGroup(uid, newGroupName, newGroup_img):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO chat_groups (uid, name, group_img) VALUES (%s, %s, %s);"
            cur.execute(sql, (uid, newGroupName, newGroup_img))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


    
    # グループ編集
    @staticmethod
    def updateGroup(uid, newGroupName, newGroup_img, gid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE chat_groups SET uid=%s, name=%s, group_img=%s WHERE id=%s;"
            cur.execute(sql, (uid, newGroupName, newGroup_img, gid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


    
    # グループ削除
    @staticmethod
    def deleteGroup(gid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM chat_groups WHERE id=%s;"
            cur.execute(sql, (gid,))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


    
    # メッセージを取得
    @staticmethod
    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            # テストのため、uid='970af84c-dd40-47ff-af23-282b72b7cca8'　（本来はuid=%s）
            sql = "SELECT id,u.uid, user_name, content FROM messages AS m INNER JOIN users As u ON m.uid='970af84c-dd40-47ff-af23-282b72b7cca8' WHERE cid=%s;"
            cur.execute(sql, (cid,))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


    
    # メッセージ追加
    @staticmethod
    def createMessage(uid, gid, content):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, gid, content) VALUES(%s,%s,%s);"
            cur.execute(sql, (uid, gid, content))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()


    
    # メッセージ更新
    @staticmethod
    def updateMessage(content, mid):
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "UPDATE messages SET content=%s WHERE mid=%s;"
                cur.execute(sql, (content, mid))
                conn.commit()
            except Exception as e:
                print(f'エラーが発生しています: {e}')
                abort(500)
            finally:
                cur.close()
                conn.close()


    
    # メッセージ削除
    @staticmethod
    def deleteMessage(mid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE mid=%s;"
            cur.execute(sql, (mid,))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            cur.close()
            conn.close()
