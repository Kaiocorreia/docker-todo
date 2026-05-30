import os
import time
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://todouser:todopass@db:5432/tododb")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    for _ in range(10):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Banco de dados inicializado.")
            return
        except Exception as e:
            print(f"Aguardando banco de dados... ({e})")
            time.sleep(2)
    raise RuntimeError("Nao foi possivel conectar ao banco de dados.")


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done, created_at FROM tasks ORDER BY created_at DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = NOT done WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
