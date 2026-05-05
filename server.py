#!/usr/bin/env python3
"""
Render Health Server + Bot Launcher
Render free tier butuh HTTP endpoint aktif agar service tidak di-shutdown.
File ini menjalankan Flask health server + amp.py bot secara bersamaan.
"""
import os
import sys
import threading
import subprocess
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
BOT_STARTED = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@app.route("/")
def health():
    return jsonify({
        "status": "alive",
        "bot": "AMP Monitor",
        "started": BOT_STARTED,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

@app.route("/health")
def health_check():
    return "OK", 200

def run_bot():
    """Jalankan amp.py sebagai subprocess."""
    subprocess.run([sys.executable, "amp.py"])

if __name__ == "__main__":
    # Start bot di thread terpisah
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Start Flask server (Render butuh ini)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
