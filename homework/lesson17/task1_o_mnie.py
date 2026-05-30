from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)