from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/me')
def me():
    return "Stanisław Flak"

if __name__ == '__main__':
    app.run(debug=True)