from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import logging

app = Flask(__name__)
app.config.from_object('config.DevConfig')

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['DATABASE_USER']}:{app.config['DATABASE_PASSWORD']}@{app.config['DATABASE_URI']}:{app.config['DATABASE_PORT']}/{app.config['DATABASE_NAME']}"


# TODO: Have to add auto commit for SqlAlchemy
db = SQLAlchemy(app)

logging.basicConfig(filename=app.config['LOG_FILE'], level=app.config['LOG_TYPE'],
                    format=f'%(asctime)s  %(levelname)s  %(name)s  %(threadName)s : %(message)s')


class Subscription(db.Model):
    """
    Subscription table
    ### Ancestors
    * flask_sqlalchemy.model.Model

     #Class Attributes
    `email`
    `id'
    `subscription`
    `timestamp`

    constructor:
             # Required Email only
             def __init__(self, email, )
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    subscription = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime, default=dt.now())

    def __init__(self, email, ):
        self.email = email
        self.subscription = True


@app.route("/api/subscription", methods=['POST'])
def insert_user():
    """
    Input:
        Type: json
        example: {
                    "email": "example@gmail.com"
                 }

    Operation:
            1. add log  in log file
                  example@eail.com added to database
                  User already exist in database
            2. Add email in Database if not exist
            3. return info of email if exist in Database
    """
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
    """
    Input:
       Type: Json
       Example:
             {
                'email': "example@gmail.com"
             }
    Operation:
         1. Add logs in log file either
                    i. subscription changed
                    ii. user not exist in database
         2. Change Subscription Status<boolean> in database if email exist in database
         3. return user not exist with status code 404 if email not exist in database
    """
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
    """
    Run's Flask Application
    Create Table subscription if not exist in database
    """
    db.create_all()
    app.run()
