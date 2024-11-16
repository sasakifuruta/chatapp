# flask、必要なライブラリをインポート
from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

# models.pyからインポート
from models import dbConnect

# セッションの内容やflashメッセージを暗号化、セッション有効期間を設定
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# アカウント作成
# アプリタイトル画面の新規登録ボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_s'とした）を押した際の処理を以下に実装。
# return：新規登録画面htmlを返す。ここで、22時以降か前かの判断を実装する予定。
@app.route('/next_step_s')
def show_signup():
    return render_template('registration/signup.html')

# # 利用時間内だった場合の処理（新規登録の処理）新規登録html画面の登録ボタンを'/process_signup'としている。


@app.route('/process_signup', methods=['POST'])
# 登録フォームに入力された値を変数に格納
def process_signup_form():
    name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password')
    password2 = request.form.get('password_confirm')

#   # mailのパターン認識(バリデーション)
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
            return redirect('/')

    return render_template("/registration/hoge.html")


# ログインページの表示
# アプリタイトル画面のログインボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_l'とした）を押した際の処理を以下に実装。
# return：新規登録画面htmlを返す。ここで、22時以降か前かの判断を実装する予定。

@app.route('/next_step_l')
def show_login():
    return render_template('registration/login.html')

# 利用時間内だった場合の処理（ログインの処理）ログインhtml画面のログインボタンを'/process_login'としている。


@app.route('/process_login', methods=['POST'])
# 登録フォームに入力された値を変数に格納
def process_login_form():
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
                return redirect('/')  # '/'がホーム画面でいいか確認する
    return render_template('registration/login.html')


# ログアウト
# ハンバーガーメニューのログアウトボタンを押した際の処理。エンドポイントは'/logout'とした。
# ログアウト後は優しい母モーダルへ返す？アプリタイトル画面へ戻す？
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/next_step_l')  # 優しい母画面に返す形でいいか？


# 退会
@app.route('/withdrawal')
def withdraw_account():
    if not session.get('uid'):
        flash('ログインしてください')
        return redirect('ログインhtmlのエンドポイント')
    else:
        uid = session['uid']
        DB_user = dbConnect.getUser(uid)
        if DB_user != None:
            dbConnect.deactivateUser(uid)
            session.clear()
            flash('退会処理が完了しました。またいつでも遊びにきてね！')
            return redirect('/"アプリタイトルhtml画面のエンドポイント"')  # アプリタイトル画面のエンドポイントを確認
        else:
            flash('退会処理が失敗しました')
            return redirect("アプリタイトルhtml画面のエンドポイント")  # アプリタイトル画面に返す？
            # 処理が失敗した場合、何が問題だったのか、ユーザーにもっとわかりやすく伝えたほうがいいと思う。



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
