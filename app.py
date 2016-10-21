from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    # TODO choose between return json or use RP
    # choose between session or cookie
    return "Hello World!"


if __name__ == "__main__":
    app.run()
