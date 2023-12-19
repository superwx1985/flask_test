import os.path
import uuid

from flask import Flask, url_for, request, Blueprint, abort, flash, redirect, send_from_directory, current_app, session
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
def username():
    token = request.args.get('access_token')
    if token in sessions:
        return {"reason": "name has been change"}, 201
    else:
        return abort(401)


def get_userid(_request):
    token = _request.args.get('access_token')
    if token not in sessions:
        return abort(401)
    else:
        return sessions[token]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    userid = get_userid(request)
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
            file_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], userid)
            os.makedirs(file_dir) if not os.path.exists(file_dir) else True
            file.save(os.path.join(file_dir, filename))
            return {"reason": f"{filename} has been uploaded"}, 201
            # return redirect(url_for('test.download_file', name=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@bp.route('/uploads/<name>')
def download_file(name):
    userid = session.get('user_id', None)
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], userid), name)


if __name__ == '__main__':
    print("aaa.jpg.exe.png".split('.')[-1])
