import db
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/init_db', methods=['POST'])
def init_database():
    db.init_db()
    return "OK\n"


@app.route('/create_user', methods=['POST'])
def create_user():
    if not request.is_json:
        return "Wrong JSON\n"
    content = request.get_json()
    print(content)
    db.save_user(content)
    return "OK\n"


@app.route('/get_users', methods=['GET'])
def get_users():
    return json.dumps({"users": db.get_users()})


@app.route('/coach', methods=['POST'])
def coach():
    # return json.dumps({
    #     "type": "message",
    #     "text": "This is a reply!"
    # })
    content = request.get_json()
    text = ''.join(x for x in content['text'].split(" ")[-1].lower() if x.isalpha())
    print(content)
    if text == 'help':
        return json.dumps({
            "type": "message",
            "text": """
                    enroll - enroll tournament
                    leave - leave tournament
                    give - wait for a quick game
                    help - print help
                    """
        })
    elif text == 'enroll':  # TODO check it
        pass
    return json.dumps({
        "type": "message",
        "text": "This is a reply!"
    })
