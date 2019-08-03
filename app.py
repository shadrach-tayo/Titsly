from flask import Flask
import db

app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('config.py')


@app.route('/', methods=['GET'])
def index():

    # tips_to_return = db.get_tips()
    return 'Welcome to url shortening server'


@app.route('/tits', methods=['POST'])
def create_tit():
    pass


@app.route('/<path>', methods=['GET'])
def get_link(path):
    pass


if __name__ == "__main__":
    # db.create_connection()
    # db.drop_table()
    app.run()
