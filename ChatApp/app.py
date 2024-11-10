# チャットグループ一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/longin')
    else:
        chat_groups = dbConnect.getChat_groupsAll()
        chat_groups.reverse()
    return render_template('index.html', chat_groups=chat_groups, uid=uid)


# チャットグループの追加
@app.route('/',methods=['POST'])
def add_chat_group():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    chat_group_name = request.form.get('chat_groupTitle')
    chat_group =dbConnect.getChat_groupByName(chat_group_name)
    if chat_group == None:
        chat_group_description = request.form.get('chat_groupDescription')
        dbConnect.addChat_group(uid, chat_group_name, chat_group_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャットグループが存在しています'
        return render_template('error/error.html', error_message=error)


# チャットグループの更新
@app.route('/update_chat_group', methods=['POST'])
def update_chat_group():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = request.form.get('cid')
    chat_group_name = request.form.get('chat_groupTitle')
    chat_group_description = request.form.get('chat_groupDescription')

    dbConnect.updateChat_group(uid, channel_name, channel_description, cid)
    return redirect('/detail/{cid}'.format(cid = cid))


# チャットグループの削除
@app.route('/delete/<cid>')
def delete_chat_group(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        chat_group = dbConnect.getChat_groupById(cid)
        if chat_group["uid"] != uid:
            flash('チャットグループは作成者のみ削除可能です')
            return redirect ('/')
        else:
            dbConnect.deleteChat_group(cid)
            chat_groups = dbConnect.getChat_groupAll()
            return redirect('/')


# チャットグループ詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = cid
    chat_group = dbConnect.getChat_groupById(cid)
    messages = dbConnect.getMessageAll(cid)

    return render_template('detail.html', messages=messages, chat_group=chat_group, uid=uid)
