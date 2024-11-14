# アカウント作成
# アプリタイトル画面の新規登録ボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_s'とした）を押した際の処理を以下に実装。時間を取得し、条件分岐。
@app.route('/next_step_s')
def show_signup():
    now = datetime.datetime.now()
    now_hour = now.hour
    if (22 <= now_hour < 24) or (0 <= now_hour < 6):
        return render_template('anger-mom.html')
    else:
        return render_template("新規登録html画面")


# ログインページの表示
# アプリタイトル画面のログインボタンを押すと、優母モーダル画面が表示される。その画面の「続ける」ボタン（エンドポイント'/next_step_l'とした）を押した際の処理を以下に実装。時間を取得し、条件分岐。

@app.route('/next_step_l')
def show_login():
    now = datetime.datetime.now()
    now_hour = now.hour
    if (22 <= now_hour < 24) or (0 <= now_hour < 6):
        return render_template('anger-mom.html')
    else:
        return render_template("ログインhtml画面")
