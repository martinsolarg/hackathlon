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


@app.route('/get_users_tour/<sport>', methods=['GET'])
def get_users_tour(sport):
    return json.dumps({"users": db.get_users_tournament(sport)})


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
    sport = ''.join(x for x in content['text'].split(" ")[-2].lower() if x.isalpha())
    print(content)
    if text != 'help' and sport.lower() not in db.config["T_SPORT"]:
        return json.dumps({
            "type": "message",
            "text": f"Invalid sport name, sports: {db.config['T_SPORT']}"
        })
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
    elif text == 'enroll':
        if not db.tournament(content, sport):
            return json.dumps({
                "type": "message",
                "text": "You are already in tournament!"
            })
        return json.dumps({
            "type": "message",
            "text": f"You are in {sport} tournament!"
        })
    elif text == 'leave':
        db.remove_user(content, sport)
        return json.dumps({
            "type": "message",
            "text": "You left tournament!"
        })
    elif text == 'give':
        player2 = db.waitlist(content)
        if player2:
            return json.dumps({
                "type": "message",
                "text": f"new match {content['from']['name']}:{player2}"
            })
        return json.dumps({
            "type": "message",
            "text": "You left tournament!"
        })
    else:
        return json.dumps({
            "type": "message",
            "text": "Wat?"
        })

