from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/me')
def me():
    return "Stanisław Flak"

@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    suma = num1 + num2
    return f"Wynik to: {suma}"

@app.route('/movies')
def movies():

    favorite_movies = [
        "Skazani na Shawshank",
        "Zielona Mila",
        "Gladiator",
        "Interstellar",
        "Incepcja"
    ]

    page_title = "Moje ulubione filmy"

    return render_template(
        "movies.html",
        movies=favorite_movies,
        page_title=page_title
    )
    
@app.route('/book')
def book():

    favorite_book = {
        "title": "Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937
    }

    return render_template(
        "book.html",
        book=favorite_book
    )    
    
@app.route('/gallery')
def gallery():

    images = [
        {
            "url": "https://picsum.photos/id/1015/300/200",
            "caption": "Góry i jezioro"
        },
        {
            "url": "https://picsum.photos/id/1025/300/200",
            "caption": "Pies"
        },
        {
            "url": "https://picsum.photos/id/1035/300/200",
            "caption": "Krajobraz"
        }
    ]

    return render_template(
        "gallery.html",
        images=images
    )
    
@app.route('/products')
def products():

    products_list = Product.query.all()

    return render_template(
        "products.html",
        products=products_list
    )

if __name__ == '__main__':
    app.run(debug=True)