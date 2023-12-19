import os.path
from flaskr.auth import login_required

from flask import Flask, url_for, request, Blueprint, abort, flash, redirect, send_from_directory, current_app, session
from werkzeug.utils import secure_filename

bp = Blueprint('file', __name__, url_prefix='/file')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']



@bp.route('/file_upload', methods=['GET', 'POST'])
@login_required
def file_upload():
    if request.method == 'POST':
        user_id = session.get('user_id')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            prefix_path = secure_filename(str(user_id))
            file_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], prefix_path)
            os.makedirs(file_dir) if not os.path.exists(file_dir) else True
            file.save(os.path.join(file_dir, filename))
            # return {"reason": f"{filename} has been uploaded"}, 201
            return redirect(url_for('file.download_file', prefix_path=prefix_path, filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@login_required
@bp.route('/uploads/<prefix_path>/<filename>')
def download_file(prefix_path, filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], prefix_path), filename)


if __name__ == '__main__':
    pass
