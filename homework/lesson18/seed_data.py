from datetime import datetime, timedelta

from app import app, db, User, Room, Booking


with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(name="Jan Kowalski", department="IT")
    user2 = User(name="Anna Nowak", department="HR")
    user3 = User(name="Piotr Wiśniewski", department="Marketing")
    admin = User(name="Admin Systemu", department="Admin", is_admin=True)

    room1 = Room(name="Sala A")
    room2 = Room(name="Sala B")

    db.session.add_all([user1, user2, user3, admin, room1, room2])
    db.session.commit()

    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    bookings = [
        Booking(title="Spotkanie zespołu", room=room1, user=user1, start_time=now - timedelta(days=1, hours=2)),
        Booking(title="Code review", room=room1, user=user1, start_time=now - timedelta(days=2, hours=1)),
        Booking(title="Rozmowa HR", room=room2, user=user2, start_time=now - timedelta(days=3, hours=3)),
        Booking(title="Prezentacja marketingowa", room=room2, user=user3, start_time=now - timedelta(days=4, hours=4)),
        Booking(title="Planning sprintu", room=room1, user=user1, start_time=now - timedelta(days=5, hours=5)),
        Booking(title="Szkolenie", room=room2, user=user2, start_time=now - timedelta(days=6, hours=2)),
    ]

    db.session.add_all(bookings)
    db.session.commit()

    print("Baza zresetowana i dane testowe dodane.")
