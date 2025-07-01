# cli/backend.py

import sys
import json
import yaml
import traceback
from pathlib import Path

from utils.logger import get_logger
from utils.error_handler import handle_failure, rollback, save_state, load_state
from core.java.main.generator import generate_java_project  # Java first

logger = get_logger("backend")

STATE_FILE = ".genapp_state.json"

def generate_backend(file, language, project_name, deploy_aws, auth, resume):
    try:
        logger.info("Starting backend generation...")
        state = load_state(STATE_FILE) if resume else {}

        # === Step 1: Load Entity Config ===
        if not resume or "parsed" not in state:
            entities = load_entity_file(file)
            state["parsed"] = True
            state["entities"] = entities
            save_state(STATE_FILE, state)
        else:
            entities = state["entities"]

        # === Step 2: Validate Language Support ===
        if language not in ["java", "python", "go", "ts"]:
            raise Exception(f"Unsupported language: {language}")

        # === Step 3: Generate Project Based on Language ===
        if not resume or "generated" not in state:
            if language == "java":
                generate_java_project(entities, project_name, deploy_aws, auth)
            # Placeholder: Add Python/Go/TS here later
            state["generated"] = True
            save_state(STATE_FILE, state)

        logger.info(f"✅ Backend generation completed for project: {project_name}")

    except Exception as e:
        logger.error("❌ Generation failed: " + str(e))
        traceback.print_exc()
        handle_failure(str(e))
        rollback(project_name)
        sys.exit(1)


def load_entity_file(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Entity file not found: {file_path}")

    logger.info(f"Loading entity definition from: {file_path}")

    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    elif file_path.endswith(".json"):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise Exception("Entity file must be .json or .yaml")