from flask import Flask, request, render_template, redirect, send_file, make_response
import sqlite3
import os
import subprocess
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = './static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Connect to DB
def get_db_connection():
    conn = sqlite3.connect('vulnerable.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def remove_headers(response):
    # Insecure: Removing security headers
    response.headers['Content-Security-Policy'] = ''
    response.headers['X-Frame-Options'] = ''
    response.headers['X-Content-Type-Options'] = ''
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Auth Bypass: Doesn't validate credentials
        return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    file = request.args.get('file', 'secret.txt')  # Path traversal
    try:
        return send_file(f'./static/{file}')
    except Exception:
        return "File not found", 404

@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL Injection
    user = conn.execute(query).fetchone()
    conn.close()
    if user:
        return dict(user)
    return {'error': 'User not found'}, 404

@app.route('/ping')
def ping():
    host = request.args.get('host', '127.0.0.1')
    command = f"ping -c 1 {host}"  # Command Injection
    result = subprocess.getoutput(command)
    return f"<pre>{result}</pre>"

@app.route('/search')
def search():
    q = request.args.get('q', '')
    return render_template('search.html', query=q)  # XSS possible

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))  # No validation
        return f'Uploaded! <a href="/static/uploads/{file.filename}">{file.filename}</a>'
    return render_template('upload.html')

@app.route('/redirect')
def open_redirect():
    url = request.args.get('url', '/')
    return redirect(url)  # Open Redirect

@app.route('/ssrf')
def ssrf():
    url = request.args.get('url', '')
    try:
        r = requests.get(url)
        return r.text[:500]
    except:
        return 'Error fetching URL'

# Hardcoded API Key (for scanning)
API_KEY = "SECRET-API-KEY-12345"

# TLS key (exposed for scanning)
PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7z7...fake_key...A23=
-----END RSA PRIVATE KEY-----
'''

if __name__ == '__main__':
    app.run(debug=True)
