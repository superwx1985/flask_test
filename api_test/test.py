from flask import Flask, url_for, request, Blueprint, abort

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
        token = "token_{}".format(userid)
        sessions[token] = userid
        return {"token": token}
    else:
        return abort(403)


@bp.route('/username', methods=["GET", "POST"])
def name():
    token = request.args.get('access_token')
    if token in sessions:

        return {"reason": "name has been change"}, 201
    else:
        return abort(403)

