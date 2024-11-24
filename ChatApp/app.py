# flask、必要なライブラリをインポート
from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from datetime import timedelta
from werkzeug.utils import secure_filename
import datetime
import time
from zoneinfo import ZoneInfo
import hashlib
import uuid
import re
import os


# models.pyからインポート
from models import dbConnect

# セッションの内容やflashメッセージを暗号化、セッション有効期間を設定
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# =====================================
# 全画面共通
# =====================================
# 22時〜６時まで全ての画面鬼母
def handle_time():
    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    now_hour = now.hour
    if (2 <= now_hour < 6):  # テスト
        # if (22 <= now_hour < 24) or (0 <= now_hour < 6):
        # return render_template(nighttime='anger-mon.html')
        return render_template('anger-mon.html')
    # else:
    return None
    # return render_template(daytime)


# セッションを確認しアクティブなユーザを取得
def session_check():
    uid = session.get('uid')
    if uid is None:
        return render_template('registration/login.html')
    else:
        DB_user = dbConnect.getUserById(uid)
        return DB_user


# =========================
# 画像関連
# =========================

# 拡張子を確認し、ファイル名を付ける
def generate_filename(file):
    origin_filename = file.filename
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    extension = origin_filename.rsplit('.', 1)[-1].lower()
    if extension in ALLOWED_EXTENSIONS:
        filename = secure_filename(origin_filename)
        timestamp = int(time.time())
        return f"{timestamp}_{filename}"
    else:
        flash('画像を選んでね', 'flash ng')
        return 'Not img'


# プロフィール画像をフォルダに保存する
def profile_img_save(template):
    # 画像の保存先ディレクトリ
    PROFILE_IMG_FOLDER = 'static/img/profile_img'
    app.config[PROFILE_IMG_FOLDER] = PROFILE_IMG_FOLDER
    profile_img = None
    if 'profile_img' in request.files:
        file = request.files['profile_img']
        if file:
            filename = generate_filename(file)
            # 拡張子が画像でない場合　
            if filename == 'Not img':
                return redirect(url_for(template))
            file.save(os.path.join(app.config[PROFILE_IMG_FOLDER], filename))
            profile_img = f"img/profile_img/{filename}"
    return profile_img


# グループ画像をフォルダに保存する
def group_img_save(template):
    # 画像の保存先ディレクトリ
    GROUP_IMG_FOLDER = 'static/img/group_img'
    app.config[GROUP_IMG_FOLDER] = GROUP_IMG_FOLDER
    group_img = None
    if 'group_img' in request.files:
        file = request.files['group_img']
        if file:
            filename = generate_filename(file)
            # 拡張子が画像でない場合　
            if filename == 'Not img':
                return redirect(url_for(template))
            file.save(os.path.join(app.config[GROUP_IMG_FOLDER], filename))
            group_img = f"img/group_img/{filename}"
    return group_img


# DBの画像パスを更新するときに、フォルダにある古い画像を削除する
def delete_img(category, id):
    if category == 'profile':
        img_path = dbConnect.getUserById(id)['profile_img']
    elif category == 'group':
        img_path = dbConnect.getGroupById(id)['group_img']
    os.remove(f'static/{img_path}')
    print(f'img_path>>{img_path}')
    return 'delete_img OK'


# 退会した人の画像をフォルダから削除する
def delete_users_img(uid):
    profile_img = dbConnect.getUserById(uid)['profile_img']
    print(f'プロフィール写真を削除>>{profile_img}')
    print(f'static/{profile_img}')
    os.remove(f'static/{profile_img}')
    users_group_images = dbConnect.getGroupAllByCreateUer(uid)
    for group_image in users_group_images:
        print(f'グループ写真を削除>>{group_image}')
        os.remove(f'static/{group_image}')
    return 'delete_img OK'


# ============================
# 認証機能
# ============================

# home.htmlにアクセスするためのエンドポイントの指定
@app.route("/home")
def home():
    uid = session.get("uid")
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    DB_user = dbConnect.getUserById(uid)
    profile_img = DB_user["profile_img"]
    return render_template("home.html", profile_img=profile_img)


# apptitle.htmlにアクセスするためのエンドポイントの指定
@app.route("/apptitle")
def apptitle():
    return render_template("apptitle.html")


# アカウント作成 >> handle_time関数を適用
@app.route('/next_step_s')
def show_signup():
    if handle_time() == None:
        return render_template('registration/signup.html')
    return handle_time()


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
        flash('まだ書いてないところがあるよ！', 'flash ng')
    elif not re.match(regex, email):
        flash('メールアドレスの書き方がちょっと違うみたいだよ！', 'flash ng')
    elif password1 != password2:
        flash('パスワードが同じじゃないみたいだよ！', 'flash ng')
    # elif パスワードの強度判定
    else:
        # PWをハッシュ化。まだ脆弱性あり。
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        # emailをキーにDBを検索
        DBuser = dbConnect.getUser(email)
        # DBに登録済みの場合
        if DBuser != None:
            flash('もう登録されてるみたいだよ！', 'flash ng')
        # 新規ユーザーとして登録
        else:
            dbConnect.createUser(uid, name, email, password)
            user_id = str(uid)
            session['uid'] = user_id
            return redirect(url_for("home"))
    return render_template("/registration/signup.html")


# ログインページの表示 >> handle_time関数を適用
@app.route('/next_step_l')
def show_login():
    if handle_time() == None:
        return render_template('registration/login.html')
    return handle_time()


# 利用時間内だった場合の処理（ログインの処理）ログインhtml画面のログインボタンを'/process_login'としている。
@app.route('/process_login', methods=['POST'])
# 登録フォームに入力された値を変数に格納
def process_login_form():
    email = request.form.get('email')
    password = request.form.get('password')

    # 入力漏れの確認
    if email == '' or password == '':
        flash('まだ書いてないところがあるよ！', 'flash ng')
    else:
        # DBからemailをキーに情報を取得
        user = dbConnect.getUser(email)
        if user == None:
            flash('このユーザーはまだ登録されてないみたいだよ！', 'flash ng')
        else:
            # 入力されたPWをハッシュ化し、DBから取得した情報と照合
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードがちがうみたいだよ！', 'flash ng')
            else:
                session['uid'] = user["uid"]
                return redirect(url_for("home"))
    return render_template('registration/login.html')


# ログアウト
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for("apptitle"))


# 退会ページの表示
@app.route('/withdrawal')
def show_withdrawal():
    # uid = session.get("uid")
    uid = '34de9b76-bbd3-44cc-9d26-079ebee34296'
    DB_user = dbConnect.getUserById(uid)
    profile_img = DB_user["profile_img"]
    return render_template('disactive.html', profile_img=profile_img)


# 退会処理
# @app.route('/withdrawal', methods=['POST'])
# def withdraw_account():
#     if not session.get('uid'):
#         flash('ログインしてね！', 'flash caution')
#         return redirect(url_for("show_withdrawal"))
#     else:
#         uid = session['uid']
#         DB_user = dbConnect.getUser(uid)
#         if DB_user != None:
#             if delete_users_img(DB_user) == 'delete_img OK':
#                 dbConnect.deactivateUser(uid)
#                 session.clear()
#                 # print('退会完了です')
#                 flash('退会処理が完了しました。またいつでも遊びにきてね！', 'flash ok')
#                 return redirect(url_for("apptitle"))
#         else:
#             flash('退会できませんでした。もう一度やってみてね！', 'flash ng')
#             return redirect(url_for("show_withdrawal"))  # とりあえず退会画面にリダイレクト。
#             # 処理が失敗した場合、何が問題だったのか、ユーザーにもっとわかりやすく伝えたほうがいいと思う。
#         return redirect(url_for("show_withdrawal"))

# テスト用！！
@app.route('/withdrawal', methods=['POST'])
def withdraw_account():
    uid = '34de9b76-bbd3-44cc-9d26-079ebee34296'
    # DB_user = dbConnect.getUserById(uid)
    if delete_users_img(uid) == 'delete_img OK':
        dbConnect.deactivateUser(uid)
        session.clear()
        print('退会完了です')
        flash('退会処理が完了しました。またいつでも遊びにきてね！', 'flash ok')
        return redirect(url_for("apptitle"))
    else:
        flash('退会できませんでした。もう一度やってみてね！', 'flash ng')
        return redirect(url_for("show_withdrawal"))


# アカウント内容画面の表示
@app.route('/update_profile')
def update_profile():
    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    now_hour = now.hour
    if (22 <= now_hour < 24) or (0 <= now_hour < 6):
        return render_template('anger-mon.html')
    else:
        # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
        uid = session.get("uid")
        DB_user = dbConnect.getUserById(uid)
        name = DB_user["user_name"]
        email = DB_user["email"]
        profile_img = DB_user["profile_img"]
        return render_template('update_profile.html',
                                user_name=name,
                                email=email,
                                profile_img=profile_img)


# アカウント変更処理
@app.route('/update_profile', methods=['POST'])
def update():
    name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password')
    password2 = request.form.get('password_confirm')

    uid = session.get("uid")
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    DB_user = dbConnect.getUserById(uid)

    if email != None:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, email):
            flash('メールアドレスの書き方がちょっと違うみたいだよ！', 'flash ng')
            return render_template('update_profile.html')

    # if:ユーザーが入力した内容に対しての条件分岐
    if password1 != password2:
        flash('パスワードが同じじゃないみたいだよ！', 'flash ng')
        return render_template('update_profile.html')
    if password1:
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    else:
        password = DB_user["password"]
    profile_img = profile_img_save(template='/update_profile')
    if profile_img is None:
        user = dbConnect.getUserById(uid)
        profile_img = user['profile_img']
    dbConnect.updateUser(name, email, password, profile_img, uid)
    return redirect(url_for("home"))


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
        DB_user = dbConnect.getUserById(uid)
        profile_img = None
        profile_img = DB_user['profile_img']

        chat_groups = dbConnect.getGroupAll()
        chat_groups = list(chat_groups)
        chat_groups.reverse()
        for group in chat_groups:
            group['group_img'] = group['group_img']
        return render_template('group.html', groups=chat_groups, profile_img=profile_img)


# チャットグループの追加画面の表示
@app.route('/create_group')
def create_group():
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get("uid")
    DB_user = dbConnect.getUserById(uid)
    profile_img = None
    profile_img = DB_user['profile_img']
    if uid is None:
        return redirect('/process_login')
    return render_template('create_group.html', profile_img=profile_img)


# チャットグループの追加
@app.route('/create_group', methods=['POST'])
def add_chat_group():
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    action = request.form.get('action')
    if action == 'create-group':
        chat_group_name = request.form.get('group_name')
        if chat_group_name == '':
            flash('チャットグループの名前を付けてね！', 'flash caution')
            return redirect('/create_group')
        chat_group = dbConnect.getGroupByName(chat_group_name)
        group_img = group_img_save(template='/create_group')
        if chat_group == None:
            dbConnect.addGroup(uid, chat_group_name, group_img)
            return redirect('/groups')
        else:
            flash('同じ名前のチャットグループがもうあるみたいだよ！', 'flash ng')
            return redirect('/create_group')
    return redirect('/groups')


# チャットグループ編集画面の表示
@app.route('/edit_group', methods=['POST'])
def edit_group():
    cid = request.form.get('cid')
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get("uid")
    DB_user = dbConnect.getUserById(uid)
    profile_img = None
    profile_img = DB_user['profile_img']

    if uid is None:
        return redirect('/process_login')
    group = dbConnect.getGroupById(cid)
    return render_template('edit_group.html',
                            cid=cid,
                            group=group,
                            profile_img=profile_img)


# チャットグループの更新と削除
@app.route('/update_chat_group', methods=['POST'])
def update_chat_group():
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    action = request.form.get('action')
    cid = request.form.get('cid')

    # 更新
    if action == 'update':
        chat_group_name = request.form.get('chat_groupTitle')
        # 画像の更新があれば
        group_img = group_img_save(template='/edit_group')
        # 変更前の画像があれば
        old_file = dbConnect.getGroupById(cid)['group_img']
        if old_file:
            delete_img('group', cid)
        dbConnect.updateGroup(uid, chat_group_name, group_img, cid)
    # 削除
    elif action == 'delete':
        chat_group = dbConnect.getGroupById(cid)
        if chat_group["uid"] != uid:
            flash('チャットグループは作った人だけが削除できるよ！', 'flash ng')
        dbConnect.deleteGroup(cid)
    return redirect('/groups')


# ======================
# メッセージ機能
# =======================

# チャット画面表示
@app.route('/group/<cid>')
def message(cid):
    uid = session.get('uid')
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'  # テスト用
    DB_user = dbConnect.getUserById(uid)
    if DB_user is None:
        return redirect('/login')
    profile_img = None
    profile_img = DB_user['profile_img']
    user_name = DB_user['user_name']
    user_id = DB_user['uid']
    group_name = dbConnect.getGroupById(cid)
    messages = dbConnect.getMessageAll(cid)
    for message in messages:
        sender = dbConnect.getUserById(message['uid'])
        message['sender_name'] = sender['user_name']
    return render_template('chat.html',
                            user_name=user_name,
                            user_id=user_id,
                            profile_img=profile_img,
                            messages=messages,
                            group_name=group_name,
                            cid=cid)


# メッセージの投稿
@app.route('/post_message', methods=['POST'])
def add_message():
    uid = session.get('uid')
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'  # テスト用
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
    # uid = '970af84c-dd40-47ff-af23-282b72b7cca8'  # テスト用
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
