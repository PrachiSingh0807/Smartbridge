from flask import Flask, render_template, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    # Example logic to just show SQL connection works
    if os.path.exists(DATABASE):
        cur = get_db().cursor()
        cur.execute("SELECT COUNT(*) FROM electricity_consumption")
        record_count = cur.fetchone()[0]
    else:
        record_count = 0
    return render_template('index.html', count=record_count)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
