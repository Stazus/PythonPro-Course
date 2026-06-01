from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import event, func
from datetime import datetime, timedelta
from uuid import uuid4
from dateutil.rrule import rrule, WEEKLY
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
    department = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="confirmed")

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    room = db.relationship("Room")
    user = db.relationship("User")
    
    recurrence_rule = db.Column(db.String(50))
    series_id = db.Column(db.String(36))
        
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
@event.listens_for(Booking, "after_insert")
def create_notifications_after_booking(mapper, connection, target):
    admin = User.query.filter_by(is_admin=True).first()

    notifications = []

    if admin:
        notifications.append(
            Notification(
                user_id=admin.id,
                message=f"Nowa rezerwacja: {target.title}"
            )
        )

    notifications.append(
        Notification(
            user_id=target.user_id,
            message=f"Przypomnienie: rezerwacja '{target.title}' została utworzona"
        )
    )

    db.session.add_all(notifications)


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

@app.route("/dashboard")
def dashboard():
    thirty_days_ago = datetime.now() - timedelta(days=30)

    bookings_by_department = (
        db.session.query(
            User.department,
            func.count(Booking.id).label("booking_count")
        )
        .join(Booking)
        .group_by(User.department)
        .all()
    )

    popular_hours = (
        db.session.query(
            func.extract("dow", Booking.start_time).label("day_of_week"),
            func.extract("hour", Booking.start_time).label("hour"),
            func.count(Booking.id).label("booking_count")
        )
        .group_by("day_of_week", "hour")
        .order_by("day_of_week", "hour")
        .all()
    )

    daily_trend = (
        db.session.query(
            func.date(Booking.start_time).label("date"),
            func.count(Booking.id).label("booking_count")
        )
        .filter(Booking.start_time >= thirty_days_ago)
        .group_by("date")
        .order_by("date")
        .all()
    )

    return jsonify({
        "bookings_by_department": [
            {
                "department": row.department,
                "booking_count": row.booking_count
            }
            for row in bookings_by_department
        ],
        "popular_hours_heatmap": [
            {
                "day_of_week": int(row.day_of_week),
                "hour": int(row.hour),
                "booking_count": row.booking_count
            }
            for row in popular_hours
        ],
        "daily_trend_last_30_days": [
            {
                "date": str(row.date),
                "booking_count": row.booking_count
            }
            for row in daily_trend
        ]
    })
    
@app.route("/dashboard-view")
def dashboard_view():
    bookings_by_department = (
        db.session.query(
            User.department,
            func.count(Booking.id).label("booking_count")
        )
        .join(Booking)
        .group_by(User.department)
        .all()
    )

    labels = [row.department for row in bookings_by_department]
    values = [row.booking_count for row in bookings_by_department]

    return render_template(
        "dashboard.html",
        labels=labels,
        values=values
    )
    
@app.route("/api/notifications")
def get_notifications():
    notifications = Notification.query.filter_by(is_read=False).all()

    return jsonify([
        {
            "id": notification.id,
            "user_id": notification.user_id,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for notification in notifications
    ])


@app.route("/api/notifications/<int:notification_id>/read", methods=["POST"])
def mark_notification_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    notification.is_read = True
    db.session.commit()

    return jsonify({
        "message": "Powiadomienie oznaczone jako przeczytane",
        "notification_id": notification.id
    })
    
@app.route("/api/bookings/recurring", methods=["POST"])
def create_recurring_booking():

    series_id = str(uuid4())

    user = User.query.first()
    room = Room.query.first()

    start_date = datetime.now()

    bookings = []

    for booking_date in rrule(
        WEEKLY,
        dtstart=start_date,
        count=12
    ):
        booking = Booking(
            title="Cykliczne spotkanie",
            start_time=booking_date,
            room=room,
            user=user,
            recurrence_rule="WEEKLY",
            series_id=series_id
        )

        bookings.append(booking)

    db.session.add_all(bookings)
    db.session.commit()

    return jsonify({
        "message": "Utworzono serię rezerwacji",
        "series_id": series_id,
        "count": len(bookings)
    })
    
@app.route("/api/bookings/<int:booking_id>/cancel", methods=["POST"])
def cancel_single_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = "cancelled"
    db.session.commit()

    return jsonify({
        "message": "Anulowano pojedynczą rezerwację",
        "booking_id": booking.id,
        "status": booking.status
    })
    
@app.route("/api/bookings/series/<series_id>/cancel", methods=["POST"])
def cancel_booking_series(series_id):
    bookings = Booking.query.filter_by(series_id=series_id).all()

    if not bookings:
        return jsonify({
            "error": "Nie znaleziono serii rezerwacji"
        }), 404

    for booking in bookings:
        booking.status = "cancelled"

    db.session.commit()

    return jsonify({
        "message": "Anulowano całą serię rezerwacji",
        "series_id": series_id,
        "cancelled_count": len(bookings)
    })

if __name__ == "__main__":
    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", count_queries)
        db.create_all()

    app.run(debug=True)
