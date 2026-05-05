#!/usr/bin/env python3
"""
Render Health Server + Bot Launcher
Render free tier butuh HTTP endpoint aktif agar service tidak di-shutdown.
File ini menjalankan Flask health server + amp.py bot secara bersamaan.
"""
import os
import sys
import threading
import traceback
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
BOT_STARTED = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
bot_status = {"running": False, "error": None}

@app.route("/")
def health():
    return jsonify({
        "status": "alive",
        "bot": "AMP Monitor",
        "bot_running": bot_status["running"],
        "bot_error": bot_status["error"],
        "started": BOT_STARTED,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

@app.route("/health")
def health_check():
    return "OK", 200

def run_bot():
    """Jalankan bot langsung (bukan subprocess)."""
    try:
        import asyncio
        # Buat event loop baru untuk thread ini
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("[SERVER] Starting AMP Monitor Bot...", flush=True)
        bot_status["running"] = True
        from amp import main
        main()
    except Exception as e:
        bot_status["running"] = False
        bot_status["error"] = str(e)
        print(f"[SERVER] Bot crashed: {e}", flush=True)
        traceback.print_exc()

if __name__ == "__main__":
    # Start bot di thread terpisah
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("[SERVER] Bot thread started", flush=True)

    # Start Flask server (Render butuh ini)
    port = int(os.environ.get("PORT", 10000))
    print(f"[SERVER] Flask starting on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
