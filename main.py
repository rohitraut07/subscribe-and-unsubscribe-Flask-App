from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import logging

app = Flask(__name__)
app.config.from_object('config.DevConfig')

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['DATABASE_USER']}:{app.config['DATABASE_PASSWORD']}@{app.config['DATABASE_URI']}:{app.config['DATABASE_PORT']}/{app.config['DATABASE_NAME']}"
db = SQLAlchemy(app)

logging.basicConfig(filename='app.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


class Subscription(db.Model):
    """Subscription table"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    subscription = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime, default=dt.now())

    def __init__(self, email, ):
        self.email = email
        self.subscription = True

@app.route("/api/subscription", methods=['POST'])
def insert_user():
    data = request.get_json()
    user = Subscription.query.filter_by(email=data['email']).first()
    if not user:
        user = Subscription(data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'HTTPCode': 200,
            'change': 'true',
            'new': 'true',
            'details': {
                'message': 'User added to database'
            }
        })
    else:
        return jsonify({
            'user': {
                'id': user.id,
                'mail': user.email,
                'timeStamp': user.timestamp,
                'subscribed': user.subscription
            },
            'HTTPCode': 200,
            'change': False,
            'new': False,
        })


@app.route("/api/subscription", methods=['PUT'])
def update_user():
    data = request.get_json()
    update_this = Subscription.query.filter_by(email=data['email']).first()
    if update_this:
        update_this.subscription = not update_this.subscription
        update_this.timestamp = dt.now()
        db.session.commit()
        return jsonify({
            'HTTPCode': 200,
            'change': 'true',
            'new': 'false',
            'details': {
                'message': 'subscription changed'
            }
        })
    else:
        return jsonify({
            'HTTPCode': 200,
            'change': False,
            'new': False,
            'details': {
                'message': 'User not exist'
            }
        })


if __name__ == "__main__":
    db.create_all()
    app.run()
