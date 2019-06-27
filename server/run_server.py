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
    print(content)
    text = ''.join(x for x in content['text'].split()[-1].lower() if x.isalpha())

    if text == 'help':
        return json.dumps({
            "type": "message",
            "text": """
                    <SPORT> enroll - enroll tournament
                    <SPORT> leave - leave tournament
                    <SPORT> give - wait for a quick game
                    help - print help
                    """
        })
    sport = content['text'].split()[-2][content['text'].split()[-2].rfind("."):]
    if text != 'help' and sport.lower() not in db.config["T_SPORT"]:
        return json.dumps({
            "type": "message",
            "text": f"Invalid sport name, sports: {db.config['T_SPORT']} not .{sport}."
        })

    if text == 'enroll':
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
        player2 = db.waitlist(content, sport)
        if player2 == 5:
            return json.dumps({
                "type": "message",
                "text": f"Hey, you are already in waitlist!"
            })
        if player2:
            return json.dumps({
                "type": "message",
                "text": f"new match @{content['from']['name']} : @{player2}"
            })
        return json.dumps({
            "type": "message",
            "text": "You are added to waitlist!"
        })
    elif text == 'round':
        pairs = db.get_tournament(content, sport)
        return json.dumps({
            "type": "message",
            "text": "You are added to waitlist!"
        })
    else:
        return json.dumps({
            "type": "message",
            "text": "Wat?"
        })

