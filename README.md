# 🔐 Security Awareness & Keylogging Simulation Tool

This project is a **cybersecurity awareness tool** that simulates keylogging attacks for educational purposes.
It securely logs keystrokes, encrypts them, and provides a **Flask-based SIEM-style dashboard** to analyze, search, and flag sensitive inputs in real time.

⚠️ **Disclaimer:** This project is strictly for **educational and security awareness purposes**. Unauthorized use of keyloggers is illegal.

---

## ✨ Features
![Uploading image.png…]()

* ✅ **Cross-Platform Keylogger** (macOS, Windows, Linux) using `pynput`
* ✅ **AES Encrypted Logs** stored in **SQLite** with `cryptography`
* ✅ **Web Dashboard (Flask)**:
  * Real-time log viewer (auto-refresh every 5 seconds)
  * Search & filter by app/keyword
  * 🚨 Sensitive keyword detection & highlighting
  * Toggle to view **only sensitive logs**
* ✅ **Resilient Design**: Handles anomalies like fast typing & backspace edits
* ✅ **Practical Use Case**: Demonstrates how **SIEM dashboards** monitor sensitive user actions

---

## 📂 Project Structure

```
Keylogger_Project/
│── keylogger.py        # Main keylogger (captures keystrokes & logs securely)
│── logger_utils.py     # Encryption & SQLite helper functions
│── web_viewer.py       # Flask dashboard (log analysis & visualization)
│── requirements.txt    # Dependencies
│── logs.db             # Encrypted log database (auto-created at runtime)
│── secret.key          # AES encryption key (auto-generated on first run)
```

---

## 🚀 Setup & Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/keylogger-project.git
cd keylogger-project
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
pip install flask
```

### 3️⃣ Run Keylogger

```bash
python3 keylogger.py
```

* Enter username: `SALMAN`
* Type in any app (Chrome, Notes, etc.)
* Quit with **Esc**

### 4️⃣ Run Web Dashboard

```bash
python3 web_viewer.py
```

Visit 👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

* Logs auto-refresh every 5s
* Sensitive keystrokes (`password`, `card`, `login`, etc.) flagged in red
* Toggle **Sensitive Only** to filter risky logs

---

## 🔎 Sensitive Keywords

The system flags keystrokes that form sensitive words such as:

* **Authentication** → `password`, `login`, `user`, `username`
* **Financial** → `card`, `credit`, `debit`, `cvv`, `pin`, `upi`, `bank`, `account`
* **Personal Identifiers** → `email`, `phone`, `mobile`, `aadhaar`
* **Security Tokens** → `otp`, `token`, `key`, `secret`

---

## 📸 Demo Preview

Here’s a sample mockup of the web dashboard:
<img width="1465" height="845" alt="Screenshot 2025-09-03 at 2 26 48 PM" src="https://github.com/user-attachments/assets/a4de8e7e-e501-4be2-8171-e9b8169a01ad" />
<img width="1465" height="845" alt="Screenshot 2025-09-03 at 2 27 10 PM" src="https://github.com/user-attachments/assets/e29957d6-53bd-414b-b10d-4cfb32076d95" />
<img width="1465" height="845" alt="Screenshot 2025-09-03 at 2 27 18 PM" src="https://github.com/user-attachments/assets/d6480055-804d-4a16-baf2-91eb46860119" />

---

## 👨‍💻 About the Author

**Mohammad Salman Ali**
Final Year B.Tech – Computer Science & Engineering
National Institute of Technology, Durgapur

* 🎓 **Google Cybersecurity Professional Certificate**
* 🛡️ Aspiring **Security Analyst** with focus on SIEM, IDS, vulnerability assessment
* 📊 Led **AI/ML & Cybersecurity workshops** (Centre for Cognitive Activities, NIT Durgapur)
* 🎭 Leadership roles in **RECSTACY & AAROHAN** (flagship fests of NIT Durgapur)
* 🏅 CBSE Chemistry Topper (Oman), Inter-NIT Handball Vice Captain

🔗 [LinkedIn](https://www.linkedin.com/in/mohdsalmanali/)
🔗 [GitHub](https://github.com/mo-salman-xo)
🔗 [Code360 Profile](https://www.naukri.com/code360/profile/salmanxo)

---


