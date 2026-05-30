from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True)