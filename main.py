from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import logging

app = Flask(__name__)
app.config.from_object('config.DevConfig')

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['DATABASE_USER']}:{app.config['DATABASE_PASSWORD']}@{app.config['DATABASE_URI']}:{app.config['DATABASE_PORT']}/{app.config['DATABASE_NAME']}"
db = SQLAlchemy(app)

logging.basicConfig(filename=app.config['LOG_FILE'], level=app.config['LOG_TYPE'],
                    format=f'%(asctime)s  %(levelname)s  %(name)s  %(threadName)s : %(message)s')


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
        app.logger.info('%s : successfully subscribed', user.email)
        return jsonify({
            'status': 201,
            'change': 'true',
            'new': 'true',
            'details': {
                'message': 'User added to database'
            }
        })
    else:
        app.logger.info('%s : User already exist', user.email)
        return jsonify({
            'user': {
                'id': user.id,
                'mail': user.email,
                'timeStamp': user.timestamp,
                'subscribed': user.subscription
            },
            'status': 200,
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
        app.logger.warning('%s : Subscription Changed', data['email'])
        return jsonify({
            'status': 200,
            'change': 'true',
            'new': 'false',
            'details': {
                'message': 'subscription changed'
            }
        })
    else:
        app.logger.warning('%s : User not exist', data['email'])
        return make_response(jsonify({
            'status': 404,
            'change': False,
            'new': None,
            'details': {
                'message': 'User not exist'
            }
        }), 404)


if __name__ == "__main__":
    db.create_all()
    app.run()
