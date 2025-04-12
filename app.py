from flask import Flask, request, render_template, redirect, send_file, make_response, url_for
import sqlite3
import os
import subprocess
import requests
import platform
from urllib.parse import urlparse


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

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    lab = request.args.get('lab', '1')  # Default to Lab 1

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if lab == '1':
            # Lab 1: No validation at all (broken auth)
            # Always redirect to Lab 2 after solving Lab 1
            return redirect('/login?lab=2')

        elif lab == '2':
            # Lab 2: Hardcoded credential check
            if username == 'admin' and password == 'admin123':
                # Redirect to Lab 3 after solving Lab 2
                return redirect('/login?lab=3')
            else:
                return render_template('login.html', error='Invalid credentials', lab=lab)

        elif lab == '3':
            # Lab 3: SQL Injection vulnerability
            conn = get_db_connection()
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            user = conn.execute(query).fetchone()
            conn.close()

            if user:
                # Redirect to /admin after solving Lab 3
                return redirect('/admin')
            else:
                return render_template('login.html', error='Invalid credentials', lab=lab)

    return render_template('login.html', lab=lab)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    lab = request.args.get('lab', '1')
    output = None
    error = None
    next_lab = None

    if request.method == 'POST':
        host = request.form.get('host', '').strip()

        if os.name == 'nt':  # Windows
            base_cmd = f"ping -n 1 {host}"
            cmd_args = ['ping', '-n', '1', host]
        else:  # Linux/Unix
            base_cmd = f"ping -c 1 {host}"
            cmd_args = ['ping', '-c', '1', host]

        try:
            if lab == '1':
                output = subprocess.getoutput(base_cmd)
                next_lab = '2'

            elif lab == '2':
                # Basic injection prevention
                if ";" in host or "&&" in host or "|" in host:
                    error = "Potential injection detected!"
                else:
                    output = subprocess.getoutput(base_cmd)
                    next_lab = '3'

            elif lab == '3':
                # Potential vulnerability in how we handle host inputs
                # Users might try to inject code indirectly via DNS, etc.
                # Example: Allowing them to modify environment variables or input for further command execution
                if host == "inject":
                    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output = result.stdout if result.returncode == 0 else result.stderr
                    error = "Command injection successful!"

                else:
                    result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output = result.stdout if result.returncode == 0 else result.stderr

                next_lab = None  # No more labs after Lab 3, so no redirection

        except Exception as e:
            error = str(e)

    return render_template('ping.html', lab=lab, output=output, error=error, next_lab=next_lab)


@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')

    # Simulate SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"

    print("[DEBUG] Executing query:", query)  # For visibility in console

    conn = get_db_connection()
    try:
        user = conn.execute(query).fetchone()
    except sqlite3.Error as e:
        conn.close()
        return render_template('user.html', error=f"SQL Error: {e}")
    
    conn.close()

    if user:
        return render_template('user.html', user=dict(user))
    return render_template('user.html', error="User not found")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    lab = request.args.get('lab', '1')
    output = request.args.get('output')  # for redirected success messages
    message = None
    error = None

    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        if lab == '1':
            # Lab 1: No validation at all
            file.save(filepath)
            return redirect('/upload?lab=2')

        elif lab == '2':
            # Lab 2: Basic extension check
            if filename.endswith('.png') or filename.endswith('.jpg'):
                file.save(filepath)
                return redirect('/upload?lab=3')
            else:
                error = "Only .png or .jpg files are allowed!"

        elif lab == '3':
            # Lab 3: Simulate unsafe code handling
            file.save(filepath)

            if filename.endswith('.py'):
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()

                    if "os.system" in content:
                        output_path = os.path.join(UPLOAD_FOLDER, "output.txt")
                        if os.name == "nt":
                            os.system(f"whoami > {output_path}")
                        else:
                            os.system(f"whoami > {output_path}")

                        output_message = "Code executed and output.txt generated!"
                    else:
                        output_message = "Python file uploaded, but no malicious pattern found."

                    return redirect(url_for('upload', lab=lab, output=output_message))

                except Exception as e:
                    error = f"Error reading file: {e}"
            else:
                error = "Error: File doesn't meet the injection criteria!"

    return render_template('upload.html', lab=lab, message=message, error=error, output=output)


@app.route('/ssrf', methods=['GET', 'POST'])
def ssrf():
    lab = request.args.get('lab', '1')  # Default to Lab 1
    url = request.form.get('url', '')  # Get URL from form submission
    output = None
    error = None
    next_lab = None

    if request.method == 'POST':
        # Check if the URL is not empty
        if not url:
            error = "URL cannot be empty!"  # Show error if URL is empty

        # If URL is missing a scheme, add http:// by default
        elif not urlparse(url).scheme:
            url = 'http://' + url  # Add http:// scheme if missing

        # Validate that the URL has both a scheme and a host
        elif not urlparse(url).netloc:
            error = "Invalid URL: No host supplied. Please provide a complete URL (e.g., http://example.com)."

        try:
            if not error:
                if lab == '1':
                    # Lab 1: Fetch content from external URL
                    r = requests.get(url)
                    output = r.text[:500]  # Display the first 500 characters of the fetched content
                    next_lab = '2'  # After Lab 1, move to Lab 2

                elif lab == '2':
                    # Lab 2: Try fetching internal resources (localhost/127.0.0.1)
                    if "localhost" in url or "127.0.0.1" in url:
                        r = requests.get(url)
                        output = f"Successfully fetched internal resource: {url} <br>{r.text[:500]}"
                        next_lab = '3'  # After Lab 2, move to Lab 3
                    else:
                        error = "This is an internal resource! You shouldn't be able to fetch this."
                    
                elif lab == '3':
                    # Lab 3: Access cloud metadata services (e.g., AWS metadata)
                    if "169.254.169.254" in url:
                        r = requests.get(url)
                        output = f"Metadata fetched: {url} <br>{r.text[:500]}"  # Fetch metadata
                    else:
                        error = "Attempted to access non-metadata resource."

        except Exception as e:
            error = f"Error fetching URL: {str(e)}"

    return render_template('ssrf.html', lab=lab, output=output, error=error, next_lab=next_lab)





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
