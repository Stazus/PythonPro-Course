from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import event
import time

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

query_count = 0

def count_queries(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    room = db.relationship("Room")
    user = db.relationship("User")
    



@app.route("/")
def home():
    return "Flask + PostgreSQL działa!"


@app.route("/test-db")
def test_db():
    try:
        db.session.execute(db.text("SELECT 1"))
        return "Połączenie OK!"
    except Exception as e:
        return f"Błąd połączenia: {e}"
    
@app.route("/debug/n-plus-1")
def debug_n_plus_1():
    global query_count

    # bez optymalizacji
    query_count = 0
    start = time.time()

    bookings = Booking.query.all()

    result1 = []

    for booking in bookings:
        result1.append({
            "title": booking.title,
            "room": booking.room.name,
            "user": booking.user.name
        })

    time1 = round((time.time() - start) * 1000, 2)
    queries1 = query_count

    # z joinedload
    query_count = 0
    start = time.time()

    bookings = Booking.query.options(
        joinedload(Booking.room),
        joinedload(Booking.user)
    ).all()

    result2 = []

    for booking in bookings:
        result2.append({
            "title": booking.title,
            "room": booking.room.name,
            "user": booking.user.name
        })

    time2 = round((time.time() - start) * 1000, 2)
    queries2 = query_count

    return jsonify({
        "without_optimization": {
            "queries": queries1,
            "time_ms": time1
        },
        "with_joinedload": {
            "queries": queries2,
            "time_ms": time2
        }
    })


if __name__ == "__main__":
    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", count_queries)
        db.create_all()

    app.run(debug=True)
