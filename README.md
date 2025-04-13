## VulnLab — Intentionally Vulnerable Flask App

> **⚠️ For educational and ethical hacking use only. DO NOT deploy in production.**

Welcome to **VulnLab** — a full-featured, intentionally vulnerable web application built with Flask. This app is designed for **learning**, **demonstrating**, and **practicing** common web application security flaws.

It features a **hacker terminal aesthetic**, glowing retro green UI, and a clean modular codebase for developers and security enthusiasts.

---

### Project Structure

```
vulnlab/
├── app.py                    # Flask app with common web vulnerabilities
├── init_db.py                # DB initialization script
├── vulnerable.db             # SQLite database
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── upload.html
│   ├── ssrf.html
|   ├── ping.html
|   ├── user.html
│   └── admin.html
├── static/
│   ├── css/
│   │   └── style.css         # Hacker-themed CSS
│   ├── uploads/              # Uploaded files (no filtering)
│   └── secret.txt            # Flag file (path traversal target)
```

---

### Vulnerabilities Covered

| Route              | Vulnerability                        | Category                |
|-------------------|--------------------------------------|-------------------------|
| `/login`          | Broken Authentication                | Access Control          |
| `/user?username=` | SQL Injection                        | Injection               |
| `/ping?host=`     | Command Injection                    | Injection               |
| `/admin?file=`    | Path Traversal                       | Misconfiguration        |
| `/upload`         | Insecure File Upload                 | File Handling           |
| `/search?q=`      | Reflected XSS                        | Cross-Site Scripting    |
| `/redirect?url=`  | Open Redirect                        | Unvalidated Redirects   |
| `/ssrf?url=`      | SSRF                                 | Server-Side Request Forgery |
| Headers Removed   | Missing Security Headers             | Misconfiguration        |
| Hardcoded Secrets | API Key & Private Key exposed        | Cryptographic Flaws     |

---

### Getting Started

#### Requirements
- Python 3.x
- pip

#### Installation

```bash
git clone https://github.com/Maha1503/vulnlab.git
cd vulnlab
pip install -r requirements.txt
python init_db.py
python app.py
```

Visit `http://localhost:5000` in your browser.

---

### Screenshots

> Hacker mode activated.

![screenshot](https://github.com/Maha1503/vulnerable_check_app/blob/main/Screenshot%20(280).png)
![screenshot](https://github.com/Maha1503/vulnerable_check_app/blob/main/Screenshot%20(281).png)
![screenshot](https://github.com/Maha1503/vulnerable_check_app/blob/main/Screenshot%20(282).png)

---

### Use Cases

- Security demos & workshops
- CTF-style training environments
- Practice exploitation techniques (SQLi, XSS, Command Injection, SSRF, etc.)
- Learn secure coding by fixing each flaw

---

### Legal Disclaimer

This project is for **educational** and **ethical hacking** purposes only. Do not scan or deploy this app on public-facing servers. The authors are not responsible for any misuse.

---

### Want More?

- [ ] Score-based CTF engine with flags
- [ ] Stored XSS, CSRF, JWT manipulation
- [ ] Login system with broken session logic
- [ ] Docker (optional if requested)
- [ ] Walkthrough & exploit writeups

---

### Authors & Credits

Built with ❤️ by ethical hackers, for ethical hackers.

