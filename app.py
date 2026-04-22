from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

def get_db():
    """Otevře spojení na databázi ptaci.db a nastaví row_factory."""
    db = sqlite3.connect('ptaci.db')
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ptaci ORDER BY nazev ASC')
    ptaci = cursor.fetchall()
    db.close()
    return render_template('dashboard.html', ptaci=ptaci)

if __name__ == '__main__':
    app.run(debug=True)
