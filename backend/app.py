from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Helper function to connect DB
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "Backend running successfully!"

# REGISTER API
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)


# LOGIN API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user["id"],
            "name": user["name"]
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
