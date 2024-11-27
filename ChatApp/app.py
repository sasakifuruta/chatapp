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
    if (23 <= now_hour < 24):  # テスト
        # if (22 <= now_hour < 24) or (0 <= now_hour < 6):
        return render_template('anger-mon.html')
    return None


# セッションを確認しアクティブなユーザを取得
def session_check():
    uid = session.get('uid')
    if uid is None:
        return None
    return dbConnect.getUserById(uid)


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
    if os.path.exists(f'static/{img_path}'):
        os.remove(f'static/{img_path}')
    return 'delete_img OK'


# 退会した人の画像をフォルダから削除する
def delete_users_img(uid):
    profile_img = dbConnect.getUserById(uid)['profile_img']
    os.remove(f'static/{profile_img}')
    users_group_images = dbConnect.getGroupAllByCreateUer(uid)
    for group_image in users_group_images:
        if os.path.exists(f'static/{group_image}'):
            os.remove(f'static/{group_image}')
    return 'delete_img OK'


# ============================
# 認証機能
# ============================

# home.htmlにアクセスするためのエンドポイントの指定
@app.route("/home")
def home():
    uid = session.get('uid')
    DB_user = dbConnect.getUserById(uid)
    if DB_user:
        profile_img = DB_user["profile_img"]
        return render_template("home.html", profile_img=profile_img)
    return render_template("registration/login.html")

# apptitle.htmlにアクセスするためのエンドポイントの指定
@app.route("/")
def apptitle():
    return render_template("apptitle.html")


# アカウント作成ページの表示
@app.route('/next_step_s')
def show_signup():
    if handle_time() == None:
        return render_template('registration/signup.html')
    return handle_time()


# アカウント作成処理
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
    else:
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


# ログインページの表示
@app.route('/next_step_l')
def show_login():
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        return render_template('registration/login.html')
    return redirect(url_for('home'))


# ログインの処理
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
    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')
    profile_img = DB_user["profile_img"]
    return render_template('registration/disactive.html', profile_img=profile_img)


# 退会処理
@app.route('/withdrawal', methods=['POST'])
def withdraw_account():
    DB_user = session_check()
    if DB_user is not None:
        uid = DB_user['uid']
        delete_users_img(uid)
        dbConnect.deactivateUser(uid)
        session.clear()
        flash('退会処理が完了しました。またいつでも遊びにきてね！', 'flash ok')
        return redirect(url_for("apptitle"))
    else:
        flash('退会できませんでした。もう一度ログインしてみてね！', 'flash ng')
        return render_template('registration/login.html')


# アカウント内容画面の表示
@app.route('/update_profile')
def update_profile():
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

    name = DB_user["user_name"]
    email = DB_user["email"]
    profile_img = DB_user["profile_img"]
    return render_template('registration/update_profile.html', user_name=name, email=email, profile_img=profile_img)


# アカウント変更処理
@app.route('/update_profile', methods=['POST'])
def update():
    name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password')
    password2 = request.form.get('password_confirm')

    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

    if email != None:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, email):
            flash('メールアドレスの書き方がちょっと違うみたいだよ！', 'flash ng')
            return render_template('registration/update_profile.html')

    if password1 != password2:
        flash('パスワードが同じじゃないみたいだよ！', 'flash ng')
        return render_template('registration/update_profile.html')

    if password1:
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    else:
        password = DB_user["password"]

    profile_img = profile_img_save(template='update_profile')
    uid = DB_user['uid']
    if profile_img is None:
        user = DB_user
        profile_img = user['profile_img']
    else:
        # 更新があれば前の画像を削除
        delete_img('profile', uid)
    dbConnect.updateUser(name, email, password, profile_img, uid)
    return redirect(url_for("home"))


# ============================
# チャットグループ機能
# ============================

# チャットグループ一覧ページの表示
@app.route('/groups')
def index():
    time = handle_time()
    if time:
        return time
    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

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
    time = handle_time()
    if time:
        return time
    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')
    profile_img = None
    profile_img = DB_user['profile_img']
    return render_template('create_group.html', profile_img=profile_img)


# チャットグループの追加
@app.route('/create_group', methods=['POST'])
def add_chat_group():
    time = handle_time()
    if time:
        return time
    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

    action = request.form.get('action')
    if action == 'create-group':
        chat_group_name = request.form.get('group_name')
        if chat_group_name == '':
            flash('チャットグループの名前を付けてね！', 'flash caution')
            return redirect('/create_group')
        chat_group = dbConnect.getGroupByName(chat_group_name)
        group_img = group_img_save(template='/create_group')
        if chat_group == None:
            uid = DB_user['uid']
            dbConnect.addGroup(uid, chat_group_name, group_img)
            return redirect('/groups')
        else:
            flash('同じ名前のチャットグループがもうあるみたいだよ！', 'flash ng')
            return redirect('/create_group')
    return redirect('/groups')


# チャットグループ編集画面の表示
@app.route('/edit_group', methods=['POST'])
def edit_group():
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')
    
    cid = request.form.get('cid')
    profile_img = None
    profile_img = DB_user['profile_img']
    group = dbConnect.getGroupById(cid)
    return render_template('edit_group.html',
                            cid=cid,
                            group=group,
                            profile_img=profile_img)


# チャットグループの更新と削除
@app.route('/update_chat_group', methods=['POST'])
def update_chat_group():
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')
    
    action = request.form.get('action')
    cid = request.form.get('cid')
    uid = DB_user['uid']

    # 更新
    if action == 'update':
        chat_group_name = request.form.get('chat_groupTitle')
        # 画像の更新があれば保存
        group_img = group_img_save(template='/edit_group')
        # 変更前の画像
        old_file = dbConnect.getGroupById(cid)['group_img']
        # 画像の更新があるなら、変更前の画像を削除
        if group_img and old_file:
            delete_img('group', cid)
        dbConnect.updateGroup(uid, chat_group_name, group_img, cid)
    # 削除
    elif action == 'delete':
        chat_group = dbConnect.getGroupById(cid)
        if chat_group["uid"] != uid:
            flash('チャットグループは作った人だけが削除できるよ！', 'flash ng')
        delete_img('group', cid)
        dbConnect.deleteGroup(cid)
    return redirect('/groups')


# ======================
# メッセージ機能
# =======================

# チャット画面表示
@app.route('/group/<cid>')
def message(cid):
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')
    
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
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

    message = request.form.get('message')
    cid = request.form.get('cid')
    if message:
        uid = DB_user['uid']
        dbConnect.createMessage(uid, cid, message)
    return redirect(f'/group/{cid}')


# メッセージの更新と削除
@app.route('/group/<cid>', methods=['POST'])
def update_message(cid):
    time = handle_time()
    if time:
        return time

    DB_user = session_check()
    if DB_user is None:
        flash('もう一度ログインしてね！', 'flash ng')
        return render_template('registration/login.html')

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
