import os
import secrets

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or os.environ.get("SECRET_KEY")
if not app.secret_key:
    if os.environ.get("VERCEL"):
        raise RuntimeError("Set SESSION_SECRET in the Vercel project environment.")
    app.secret_key = "local-development-only-change-before-deploying"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=bool(os.environ.get("VERCEL")),
)

if not os.environ.get("VERCEL"):
    @app.get("/<path:asset_path>")
    def local_public_asset(asset_path):
        return send_from_directory("public", asset_path)


def get_connection():
    required = ("MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE")
    if os.environ.get("VERCEL"):
        missing = [key for key in required if not os.environ.get(key)]
        if missing:
            raise RuntimeError(
                "Missing database environment variables: " + ", ".join(missing)
            )

    return pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=os.environ.get("MYSQL_DATABASE", "gacha_abelard"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


def logged_in():
    return isinstance(session.get("id"), int)


def draw_rarity(pity4, pity5):
    pity4 += 1
    pity5 += 1
    if secrets.randbelow(1_000) == 0:
        return 6, 0, pity5

    roll = secrets.randbelow(1000)

    if pity5 >= 100 or roll == 0:
        return 5, 0, 0
    if pity4 >= 10 or roll <= 90:
        return 4, 0, pity5
    return 3, pity4, pity5


def get_storage(cursor, user_id):
    cursor.execute(
        "SELECT c.name, c.rarity, c.img, uc.copies "
        "FROM user_characters uc "
        "JOIN characters c ON c.id = uc.character_id "
        "WHERE uc.user_id = %s "
        "ORDER BY c.rarity DESC, c.name",
        (user_id,),
    )
    return cursor.fetchall()


@app.get("/index.php")
@app.get("/")
def index():
    if not logged_in():
        return redirect(url_for("login"))

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username, gems, pity4, pity5 FROM users WHERE id = %s",
                (session["id"],),
            )
            user = cursor.fetchone()
    finally:
        connection.close()

    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("index.html", user=user)


@app.get("/storage")
def storage():
    if not logged_in():
        return redirect(url_for("login"))

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username FROM users WHERE id = %s", (session["id"],)
            )
            user = cursor.fetchone()
            characters = get_storage(cursor, session["id"]) if user else []
    finally:
        connection.close()

    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("storage.html", user=user, storage=characters)


@app.route("/login.php", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password FROM users WHERE username = %s",
                    (username,),
                )
                user = cursor.fetchone()
        finally:
            connection.close()

        password_hash = user["password"].encode("utf-8") if user else b""
        password_bytes = password.encode("utf-8")
        if password_hash.startswith(b"$2y$"):
            password_hash = b"$2b$" + password_hash[4:]
        if user and len(password_bytes) <= 72 and bcrypt.checkpw(
            password_bytes, password_hash
        ):
            session.clear()
            session["user"] = user["username"]
            session["id"] = user["id"]
            return redirect(url_for("index"))
        error = "Wrong username or password."

    return render_template("login.html", error=error)


@app.route("/register.php", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Username and password are required."
        elif len(password.encode("utf-8")) > 72:
            error = "Password must be 72 bytes or fewer."
        else:
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM users WHERE username = %s", (username,)
                    )
                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute(
                            "INSERT INTO users (username, password, gems) "
                            "VALUES (%s, %s, 9999999)",
                            (username, password_hash),
                        )
                if exists:
                    error = "Username already taken!"
                else:
                    connection.commit()
                    return render_template("register.html", registered=True)
            finally:
                connection.close()

    return render_template("register.html", error=error)


@app.route("/logout.php", methods=["GET", "POST"])
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("logout.html")


@app.post("/api/pull")
@app.post("/pull.php")
def pull():
    if not logged_in():
        return jsonify(error="Login required"), 401

    times = 10 if request.form.get("times") == "10" else 1
    cost = 2700 if times == 10 else 300
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT gems, pity4, pity5 FROM users WHERE id = %s FOR UPDATE",
                (session["id"],),
            )
            user = cursor.fetchone()
            if user is None:
                connection.rollback()
                session.clear()
                return jsonify(error="Login required"), 401
            if user["gems"] < cost:
                connection.rollback()
                return jsonify(error="Not enough gems"), 400

            results = []
            pity4 = user["pity4"]
            pity5 = user["pity5"]
            for _ in range(times):
                rarity, pity4, pity5 = draw_rarity(pity4, pity5)

                cursor.execute(
                    "SELECT id, name, rarity, img FROM characters "
                    "WHERE rarity = %s ORDER BY RAND() LIMIT 1",
                    (rarity,),
                )
                character = cursor.fetchone() or {
                    "name": "??",
                    "rarity": 3,
                    "img": "images/Red.png",
                }
                if "id" in character:
                    cursor.execute(
                        "INSERT INTO user_characters "
                        "(user_id, character_id, copies) VALUES (%s, %s, 1) "
                        "ON DUPLICATE KEY UPDATE copies = copies + 1",
                        (session["id"], character["id"]),
                    )
                results.append(
                    {
                        "name": character["name"],
                        "rarity": character["rarity"],
                        "img": character["img"],
                    }
                )

            new_gems = user["gems"] - cost
            cursor.execute(
                "UPDATE users SET gems = %s, pity4 = %s, pity5 = %s, "
                "pulls = pulls + %s WHERE id = %s",
                (new_gems, pity4, pity5, times, session["id"]),
            )
            storage = get_storage(cursor, session["id"])
        connection.commit()
    finally:
        connection.close()

    return jsonify(
        gems=new_gems,
        pity4=pity4,
        pity5=pity5,
        results=results,
        storage=storage,
    )


@app.get("/health")
@app.get("/test.php")
def health():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    finally:
        connection.close()
    return jsonify(status="ok", database="connected")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
