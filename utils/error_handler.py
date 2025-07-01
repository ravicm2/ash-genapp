import os
import json
import shutil
from pathlib import Path
from datetime import datetime

def handle_failure(error_msg):
    print(f"\n❌ ERROR: {error_msg}")
    log_error_to_file("global", error_msg)

def rollback(project_name):
    if not project_name:
        return
    try:
        project_path = Path(project_name)
        if project_path.exists() and project_path.is_dir():
            shutil.rmtree(project_path)
            print(f"🧹 Rolled back generated project: {project_name}")
            log_info_to_file("rollback", f"Rolled back project: {project_name}")
    except Exception as e:
        print(f"⚠️ Rollback failed: {str(e)}")
        log_error_to_file("rollback", f"Rollback failed for {project_name}: {str(e)}")

def save_state(state_file, state_data):
    try:
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
        log_info_to_file("state", f"Saved state to {state_file}")
    except Exception as e:
        handle_failure(f"Failed to save state: {str(e)}")

def load_state(state_file):
    try:
        with open(state_file, 'r') as f:
            data = json.load(f)
        log_info_to_file("state", f"Loaded state from {state_file}")
        return data
    except Exception as e:
        handle_failure(f"Failed to load state: {str(e)}")
        return {}

def log_error_to_file(context, msg):
    log_file = Path("logs") / f"{context}-errors.log"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"[{datetime.now()}] ERROR: {msg}\n")

def log_info_to_file(context, msg):
    log_file = Path("logs") / f"{context}-info.log"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"[{datetime.now()}] INFO: {msg}\n")