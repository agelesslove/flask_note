import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
DB_FILE = 'notes.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            note_id = str(uuid.uuid4())[:8]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notes (id, content) VALUES (?, ?)', (note_id, content))
            conn.commit()
            conn.close()
            return redirect(url_for('view_note', note_id=note_id))
    return render_template('index.html')

@app.route('/note/<note_id>')
def view_note(note_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM notes WHERE id = ?', (note_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return render_template('note.html', content=row[0], note_id=note_id)
    return abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)