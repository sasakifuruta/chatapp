# flask、必要なライブラリをインポート
from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from datetime import timedelta
import datetime
from zoneinfo import ZoneInfo
import hashlib
import uuid
import re

# models.pyからインポート
from models import dbConnect

# セッションの内容やflashメッセージを暗号化、セッション有効期間を設定
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# ============================
# 認証機能
# ============================

# home.htmlにアクセスするためのエンドポイントの指定
@app.route("/home")
def home():
    return render_template("home.html")


# apptitle.htmlにアクセスするためのエンドポイントの指定
@app.route("/apptitle")
def apptitle():
    return render_template("apptitle.html")


# アカウント作成
# アプリタイトル画面の新規登録ボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_s'とした）を押した際の処理を以下に実装。
# return：新規登録画面htmlを返す。ここで、22時以降か前かの判断を実装する予定。
@app.route('/next_step_s')
def show_signup():
  now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
  now_hour = now.hour
  if (22 <= now_hour < 24) or (0 <= now_hour < 6):
    return render_template('anger-mon.html')
  else:
    return render_template('registration/signup.html')


# 利用時間内だった場合の処理（新規登録の処理）新規登録html画面の登録ボタンを'/process_signup'としている。
@app.route('/process_signup', methods=['POST'])
# 登録フォームに入力された値を変数に格納
def process_signup_form():
    name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password')
    password2 = request.form.get('password_confirm')

    # mailのパターン認識(バリデーション)
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # if:ユーザーが入力した内容に対しての条件分岐
    if name == '' or email == '' or password1 == '' or password2 == '':
      flash('入力されていない項目があります')
    elif not re.match(regex, email):
      flash('メールアドレスの形式が正しくありません')
    elif password1 != password2:
      flash('二つのパスワードの値が一致していません')
    # elif パスワードの強度判定
    else:
      # PWをハッシュ化。まだ脆弱性あり。
      uid = uuid.uuid4()
      password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
      # emailをキーにDBを検索
      DBuser = dbConnect.getUser(email)
      # DBに登録済みの場合
      if DBuser != None:
        flash('すでに登録されているようです')
      # 新規ユーザーとして登録
      else:
        dbConnect.createUser(uid, name, email, password)
        user_id = str(uid)
        session['uid'] = user_id
        return redirect(url_for("home"))
    return render_template("/registration/signup.html")


# ログインページの表示
# アプリタイトル画面のログインボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_l'とした）を押した際の処理を以下に実装。
# return：新規登録画面htmlを返す。ここで、22時以降か前かの判断を実装する予定。
@app.route('/next_step_l',)
def show_login():
  now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
  now_hour = now.hour
  if (22 <= now_hour < 24) or (0 <= now_hour < 6):
    return render_template('anger-mon.html')
  else:
    return render_template('registration/login.html')


# 利用時間内だった場合の処理（ログインの処理）ログインhtml画面のログインボタンを'/process_login'としている。
@app.route('/process_login', methods=['POST'])
# 登録フォームに入力された値を変数に格納
def process_login_form():
    email = request.form.get('email')
    password = request.form.get('password')
    email = request.form.get('email')
    password = request.form.get('password')

  # 入力漏れの確認
    if email == '' or password == '':
      flash('入力されていない項目があります')
    else:
      # DBからemailをキーに情報を取得
      user = dbConnect.getUser(email)
      if user == None:
        flash('このユーザーは登録されていません')
      else:
        # 入力されたPWをハッシュ化し、DBから取得した情報と照合
        hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if hashPassword != user["password"]:
          flash('パスワードが間違っています')
        else:
          session['uid'] = user["uid"]
          return redirect(url_for("home"))
    return render_template('registration/login.html')    


# ログアウト
# ハンバーガーメニューのログアウトボタンを押した際の処理。エンドポイントは'/logout'とした。
@app.route('/logout', methods=['POST']) # home.htmlのハンバーガーメニューにログアウトボタンのエンドポイントが記述されたら紐づける。
def logout():
  session.clear()
  return redirect(url_for("apptitle"))

# 退会
# login.htmlにアクセスするためのエンドポイントの指定。セッションが無効でログインページに返したい時は必要。
@app.route("/disactive")
def disactive():
    return render_template('registration/login.html')

# 退会ページの表示
@app.route('/') # home.htmlのハンバーガーメニューに退会ボタンのエンドポイントが記述されたら紐づける。
def show_withdrawal():
    return render_template('disactive.html')


@app.route('/withdrawal', methods=['GET', 'POST'])
def withdraw_account():
  if not session.get('uid'):
    flash('ログインしてください')
    # print("セッションにuidが存在しません")
    return redirect(url_for("apptitle"))
  else:
    uid = session['uid']
    DB_user = dbConnect.getUser(uid)
    if DB_user != None:
      dbConnect.deactivateUser(uid)
      session.clear()
      # print('退会完了です')
      flash('退会処理が完了しました。またいつでも遊びにきてね！')
      return redirect(url_for("apptitle"))
    else:
      flash('退会処理が失敗しました')
      # print('退会失敗です')
      return redirect('/withdrawal') # とりあえず退会画面にリダイレクト。
      # 処理が失敗した場合、何が問題だったのか、ユーザーにもっとわかりやすく伝えたほうがいいと思う。
  # return redirect('/withdrawal')


# アカウント変更画面の表示
# テンプレートに表示するもの: user_name, email, password_length = len(password)


# アカウント変更
# 登録成功したらhomeにリダイレクト？



# ============================
# チャットグループ機能
# ============================

# チャットグループ一覧ページの表示
@app.route('/groups')
def index():
    uid = session.get("uid")
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    if uid is None:
        return redirect('/process_login')
    else:
        chat_groups = dbConnect.getGroupAll()
        chat_groups = list(chat_groups)
        chat_groups.reverse()
    # return render_template('group.html', chat_groups=chat_groups, uid=uid)
    return render_template('group.html', groups=chat_groups,)


# チャットグループの追加画面の表示
@app.route('/create_group')
def create_group():
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get("uid")
    
    if uid is None:
        return redirect('/process_login')
    # return render_template('group.html', chat_groups=chat_groups, uid=uid)
    return render_template('create_group.html')


# チャットグループの追加
@app.route('/create_group', methods=['POST'])
def add_chat_group():
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    chat_group_name = request.form.get('group_name')
    chat_group = dbConnect.getGroupByName(chat_group_name)
    group_img = "no_img"
    if chat_group == None:
        dbConnect.addGroup(uid, chat_group_name, group_img)
        return redirect('/groups')
    else:
        error = '既に同じ名前のチャットグループが存在しています'
        return render_template('error/error.html', error_message=error)


# チャットグループ編集画面の表示
@app.route('/edit_group/<cid>')
def edit_group(cid):
  # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
  uid = session.get("uid")
  if uid is None:
    return redirect('/process_login')

  group_name = dbConnect.getGroupById(cid)
  # return render_template('group.html', chat_groups=chat_groups, uid=uid)
  return render_template('edit_group.html', cid=cid, group_name=group_name)


# チャットグループ名の更新
@app.route('/update_chat_group', methods=['POST'])
def update_chat_group():
  # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
  # cid= 1
  group_img = "noimg"
  uid = session.get("uid")  
  if uid is None:
      return redirect('/login')

  cid = request.form.get('cid')
  chat_group_name = request.form.get('chat_groupTitle')

  dbConnect.updateGroup(uid, chat_group_name, group_img, cid)
  return redirect('/groups')


# チャットグループの削除
@app.route('/update_chat_group', methods=['POST'])
def delete_chat_group():
  uid = session.get("uid")
  # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
  # cid= 1
  if uid is None:
      return redirect('/login')
  else:
    cid = request.form.get('cid')
    chat_group = dbConnect.getGroupById(cid)
  if chat_group["uid"] != uid:
    flash('チャットグループは作成者のみ削除可能です')
    return redirect('/')
  else:
    dbConnect.deleteGroup(cid)
  return redirect('/groups')



# ======================
# メッセージ機能
# =======================

# チャット画面表示
@app.route('/group/<cid>')
def message(cid):
    uid = session.get('uid')
    # uid  = '970af84c-dd40-47ff-af23-282b72b7cca8' # テスト用
    DB_user = dbConnect.getUser(uid)
    if DB_user is None:
        return redirect('/login')

    group_name = dbConnect.getGroupById(cid)
    messages = dbConnect.getMessageAll(cid)
    return render_template('chat.html', user_name=DB_user, messages=messages, group_name=group_name, cid=cid)


# メッセージの投稿
@app.route('/post_message', methods=['POST'])
def add_message():
    uid = session.get('uid')
    DB_user = dbConnect.getUser(uid)
    if DB_user is None:
        return redirect('/login')

    message = request.form.get('message')
    cid = request.form.get('cid')
    if message:
        dbConnect.createMessage(uid, cid, message)
    return redirect(f'/group/{cid}')


# メッセージの更新と削除
@app.route('/group/<cid>', methods=['POST'])
def update_message(cid):
    uid = session.get('uid')
    DB_user = dbConnect.getUser(uid)
    if DB_user is None:
        return redirect('/login')

    action = request.form.get('action')
    mid = request.form.get('mid')

    # 更新
    if action == 'update':
        content = request.form.get('update-message')
        if mid and content:
            dbConnect.updateMessage(content, mid)

    # 削除
    elif action == 'delete':
        if mid:
            dbConnect.deleteMessage(mid)
    return redirect(f'/group/{cid}')




# # エラーページの表示
# @app.errorhandler(404)
# def show_error404(error):
#     return render_template('error/404.html'),404


# @app.errorhandler(500)
# def show_error500(error):
#     return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
