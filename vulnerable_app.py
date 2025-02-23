from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Simulated database connection (vulnerable to SQL injection)
def get_db_connection():
    conn = sqlite3.connect('vulnerable.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return 'Vulnerable Flask App for Git Secrets Scanning'

# SQL Injection Vulnerable Endpoint
@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL Injection risk
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

# Hardcoded API Key (for secrets scanning)
API_KEY = '12345-ABCDE-SECRET-API-KEY'

# SSL/TLS Private Key Example (for secrets scanning)
SSL_PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7z7...example_key...A23=
-----END RSA PRIVATE KEY-----
'''

# SSL/TLS Certificate Example (for secrets scanning)
SSL_CERTIFICATE = '''
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIE...example_certificate...DQ==
-----END CERTIFICATE-----
'''

if __name__ == '__main__':
    app.run(debug=True)
