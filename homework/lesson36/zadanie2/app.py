from flask import Flask, jsonify
import psutil


app = Flask(__name__)


@app.route("/health")
def health():
    memory = psutil.virtual_memory()

    return jsonify(
        {
            "status": "ok",
            "service": "health-check",
            "memory": {
                "total_mb": round(memory.total / 1024 / 1024, 2),
                "used_mb": round(memory.used / 1024 / 1024, 2),
                "available_mb": round(memory.available / 1024 / 1024, 2),
                "usage_percent": memory.percent,
            },
        }
    ), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
