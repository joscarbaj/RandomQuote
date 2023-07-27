# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect
import random
import psycopg2

app = Flask(__name__)

app.config["POSTGRES_HOST"] = 'dpg-cj084ptph6ek4q4ph2u0-a.oregon-postgres.render.com'
app.config["POSTGRES_USER"] = "tasklist_5ote_user"
app.config["POSTGRES_PASSWORD"] = "VAAXhrGus7cRPlTO1wACCKPAzAMijTda"
app.config["POSTGRES_DB"] = "tasklist_5ote"

# Function to establish a connection to the PostgreSQL database
def get_db_connection():
    connection = psycopg2.connect(
        host=app.config["POSTGRES_HOST"],
        user=app.config["POSTGRES_USER"],
        password=app.config["POSTGRES_PASSWORD"],
        database=app.config["POSTGRES_DB"],
        options="-c client_encoding=utf8"  # Configurar la codificación UTF-8
    )
    return connection

@app.route('/')
def Index():
    return render_template("index.html")

@app.route("/community")
def community():
    return "Hello"

@app.route("/services")
def services():
    return "Services"

@app.route("/contact")
def contacts():
    return render_template("contacts.html")

@app.route("/faq")
def faq():
    return "FAQ"

@app.route("/random_quote")
def random_quote():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM famosos")  # Obtener solo la columna "cita"
    data = cur.fetchall()
    data_lenght = len(data) -1
    cur.close()
    conn.close()
    rand_number = random.randint(0,data_lenght)
   
    author = data[rand_number][1]
    random_quote = data[rand_number][2]  # Obtener una cita aleatoria de la lista de datos

    return render_template("random_quote.html", quote=random_quote,author = author)


@app.route("/form", methods=["POST", "GET"])
def send_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, mail) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()
        conn.close()

        return render_template("contacts.html")
    else:
        return redirect(url_for("Index"))

if __name__ == "__main__":
    app.run(debug=False, port=50000, host="0.0.0.0")
