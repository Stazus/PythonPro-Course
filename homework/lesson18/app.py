from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


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


if __name__ == "__main__":
    app.run(debug=True)
