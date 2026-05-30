from task1_o_mnie import app, Product

with app.app_context():
    products = Product.query.all()

    for product in products:
        print(product.id, product.name, product.price)