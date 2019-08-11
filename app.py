from flask import Flask, request, jsonify, redirect
import db

app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('config.py')


@app.route('/', methods=['GET'])
def index():

    # tips_to_return = db.get_tips()
    return 'Welcome to url shortening server'


@app.route('/tits', methods=['POST'])
def create_tit():
    # if request.is_json:
    data = request.get_json()
    print(data['tinyurl'], ' = ', data['link'])

    # generate short link from long link or use short_form
    if data['tinyurl']:
        tinyurl = data['tinyurl']
    else:
        # tinyurl = generate_tinyurl(data['link'])
        # write base62 encoder algorithm that accepts alphabets(upper and lower cases)
        pass

    '''check if generated short link exists in database
    if it doesn't exist, the store short and long link in database
    '''
    try:
        saved = db.save_if_not_exist(tinyurl, data['link'])
    except Exception:
        return jsonify({'message': 'Server error: Database could not be accessed', 'error': True})

    # if it does exist send a customized error message to user
    if saved:
        json_response = {'message': 'tiny url created sucessfully',
                         'success': True, 'tinyurl': request.host_url + tinyurl}
        return jsonify(json_response)
    else:
        json_response = {
            'message': '{} is already in use, try another one'.format(data['tinyurl']), 'error': True}
        return jsonify(json_response)


@app.route('/<tinyurl>', methods=['GET'])
def get_link(tinyurl):
    '''Get link affiliated to tinyurl in the database
    and redirect response to the link
    '''
    data = db.get_link(tinyurl)
    if data:
        return redirect(data[1], code=302)
    else:
        return jsonify({'message': '{} is not a registered Tits'.format(tinyurl)})


if __name__ == "__main__":
    db.create_connection()
    # db.drop_table()
    app.run()
