from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta

from models import dbConnect


app = Flask(__name__)

# メッセージの投稿
@app.route('/message', methods=['POST'])
def add_message():
    uid = session.get('uid')
    # アクティブなユーザか
    
    if uid is None:
        return redirect('/login')
    
    message = request.form.get('message')
    cid = request.form.get('cid')
    
    if message:
        dbConnect.createMessage(uid, cid, message)
    
    return redirect(f'/detail/{cid}')

# メッセージの更新
@app.route('')



# メッセージの削除
@app.route('delete_message', methods=['POST'])
def delete_message():
    uid = session.get('uid')
    # アクティブなユーザか
    
    if uid is None:
        return redirect('/login')
    
    message_id = request.form.get('message_id')
    cid = request.form.get('cid')
    
    if message_id:
        dbConnect.delete_message(message_id)
    
    return redirect(f'/detail/{cid}')



# エラーページの表示
    @app.errorhandler(404)
    def show_error404(error):
        return render_template('error/404.html'),404
    
    
    @app.errorhandler(500)
    def show_error500(error):
        return render_template('error/500.html'),500
    
