import flask
from flask import jsonify
from datetime import datetime
import psycopg2
from datetime import datetime as dt

app = flask.Flask(__name__)
app.config.from_object('config.DevConfig')


def create_connection():
    conn = psycopg2.connect(database="mydb", user="postgres", password="3366", host="127.0.0.1", port="5432")
    return conn


@app.route("/subsriber/display/<string:email>", methods=['GET'])
def view_status(email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(f"select * from public.Subscribers where email='{email}'")
        user = cursor.fetchall()
        if user:
            connection.commit()
            connection.close()
            return jsonify({
                'user': {
                    'id': user[0][0],
                    'mail': user[0][1],
                    'timeStamp': user[0][2],
                    'subscribed': user[0][3] == 1
                },
                'HTTPCode': 200,
            })
        else:
            connection.commit()
            connection.close()
            return jsonify({
                'error': 'Invalid payload',
                'user': "False",
                'details': {
                    'message': 'User Not Found'
                },
                'HTTPCode': 400,
            })
        cursor.close()
    except:
        return jsonify({
            'HTTPCode': 500,
            'details': {
                'message': 'Internal Server Error'
            },
        })


@app.route("/subscriber/update/<string:email>", methods=['POST'])
def subscribe(email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(f"select * from public.Subscribers where email='{email}';")
        user = cursor.fetchall()
        print(user)
        if user:
            cursor.execute(
                f"UPDATE Subscribers SET status = '{not user[0][3]}', timestamp = '{dt.now()}' where email='{email}';")
            connection.commit()
            connection.close()
            return jsonify({
                'HTTPCode': 200,
                'change': 'true',
                'new': 'false',
                'details': {
                    'message': 'subscription changed'
                }
            })
        else:
            cursor.execute(f"insert into public.Subscribers (email, status) values ('{email}', 'True');")
            connection.commit()
            connection.close()
            return jsonify({
                'HTTPCode': 200,
                'change': 'true',
                'new': 'true',
                'details': {
                    'message': 'User added to database'
                }
            })
    except:
        return jsonify({
            'HTTPCode': 500,
            'details': {
                'message': 'Internal Server Error'
            },
        })


if __name__ == "__main__":
    app.run()
