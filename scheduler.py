import time
import json
import random
import subprocess
import os

def load_stats():
    try:
        with open("stats.json", "r") as f:
            return json.load(f)
    except:
        return {"answered": 0}

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        # fallback safe config
        return {
            "mode": "fixed",
            "fixed_minutes": 30,
            "min_minutes": 20,
            "max_minutes": 60,
            "enabled": False
        }

def get_wait_time(cfg):
    base = (
        cfg["fixed_minutes"] * 60
        if cfg["mode"] == "fixed"
        else random.randint(cfg["min_minutes"], cfg["max_minutes"]) * 60
    )

    stats = load_stats()
    bonus = stats.get("answered", 0) * 5 * 60   # 5 min per answer
    bonus = min(bonus, 60 * 60)                 # cap at +1 hour

    return base + bonus

print("📚 Study Nudge Scheduler started")

try:
    while True:
        cfg = load_config()

        if not cfg.get("enabled", True):
            print("🛑 Scheduler disabled via config.json")
            time.sleep(5)
            continue

        wait = get_wait_time(cfg)

        # broadcast next popup time
        with open("next_popup.json", "w") as f:
            json.dump({"timestamp": time.time() + wait}, f)

        mins = wait // 60
        print(f"⏳ Next popup in {mins} minutes")

        time.sleep(wait)

        popup_path = os.path.join(os.getcwd(), "ui", "popup.py")
        print("😈 Launching study popup")
        subprocess.run(["python", popup_path])

except KeyboardInterrupt:
    print("\n🛑 Scheduler stopped by user (Ctrl+C)")
