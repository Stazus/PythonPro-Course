from task1_o_mnie import app, db, Product

with app.app_context():
    p1 = Product(name="Laptop", price=2999.99)
    p2 = Product(name="Monitor", price=899.99)
    p3 = Product(name="Klawiatura", price=199.99)

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    print("Produkty dodane!")