from flask import Flask, url_for, request, abort

app = Flask(__name__)
sessions = dict()


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


@app.route('/login', methods=["GET"])
def login():
    userid = request.args.get('userid', '')
    secret = request.args.get('secret', '')
    d = {"123": "abc", "abc": "456"}
    if d.get(userid) == secret:
        token = "token_{}".format(userid)
        sessions[token] = userid
        return {"token": token}
    else:
        return abort(401)


@app.route('/username', methods=["GET", "POST"])
def name():
    token = request.args.get('access_token')
    if token in sessions:

        return {"reason": "name has been change"}, 201
    else:
        return abort(401)


if __name__ == '__main__':
    # with app.test_request_context():
    #     print(url_for('profile', username='John Doe', a=2))
    app.run(port=5000)
