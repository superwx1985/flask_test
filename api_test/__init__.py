from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from api_test import test
    app.register_blueprint(test.bp)

    return app


if __name__ == '__main__':
    create_app().run(port=8080)



