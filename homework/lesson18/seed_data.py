from app import app, db, User, Room, Booking

with app.app_context():
    if User.query.first():
        print("Dane już istnieją.")
    else:
        user1 = User(name="Jan Kowalski")
        user2 = User(name="Anna Nowak")

        room1 = Room(name="Sala A")
        room2 = Room(name="Sala B")

        db.session.add_all([user1, user2, room1, room2])
        db.session.commit()

        booking1 = Booking(title="Spotkanie zespołu", room=room1, user=user1)
        booking2 = Booking(title="Code review", room=room1, user=user2)
        booking3 = Booking(title="Prezentacja projektu", room=room2, user=user1)
        booking4 = Booking(title="Rozmowa rekrutacyjna", room=room2, user=user2)

        db.session.add_all([booking1, booking2, booking3, booking4])
        db.session.commit()

        print("Dane testowe dodane.")