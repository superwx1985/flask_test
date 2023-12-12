import os.path
import uuid

from flask import Flask, url_for, request, Blueprint, abort, flash, redirect
from werkzeug.utils import secure_filename

bp = Blueprint('test', __name__, url_prefix='/test')
sessions = dict()
users = {"123": "abc", "abc": "456"}


@bp.route('/hello')
def hello_world():
    return 'hello world'


@bp.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


@bp.route('/login', methods=["GET"])
def login():
    userid = request.args.get('userid', '')
    secret = request.args.get('secret', '')

    if users.get(userid) == secret:
        token = f"token_{userid}_{uuid.uuid1()}"
        sessions[token] = userid
        return {"token": token}
    else:
        return abort(401)


@bp.route('/username', methods=["GET", "POST"])
def name():
    token = request.args.get('access_token')
    if token in sessions:
        return {"reason": "name has been change"}, 201
    else:
        return abort(401)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    token = request.args.get('access_token')
    if token not in sessions:
        return abort(401)
    else:
        userid = sessions[token]
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {"reason": "No file part"}, 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {"reason": "No selected file"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_dir = os.path.join("temp_file", userid)
            os.makedirs(file_dir) if not os.path.exists(file_dir) else True
            file.save(os.path.join(file_dir, filename))
            return {"reason": f"{filename} has been uploaded"}, 201
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


if __name__ == '__main__':
    print("aaa.jpg.exe.png".split('.')[-1])
