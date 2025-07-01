# core/java/generator.py

import os
import json
import yaml
from pathlib import Path
from utils.logger import get_logger
from utils.error_handler import handle_failure, rollback, save_state, load_state

def generate_java_project(entity_path, output_dir, project_name, version, resume=False):
    logger = get_logger("java-generator", project_name, version)

    logger.info("🚀 Starting Java backend generation for '%s'", project_name)
    state_file = Path(".genapp_state.json")
    application_name = project_name.lower()

    # Load resume state if applicable
    state = load_state(state_file) if resume and state_file.exists() else {}

    try:
        # Step 1: Load entity JSON/YAML
        logger.info(f"📦 Loading entity file: {entity_path}")
        with open(entity_path, 'r') as f:
            if entity_path.endswith((".yaml", ".yml")):
                entities = yaml.safe_load(f)
            else:
                entities = json.load(f)

        entity_defs = entities.get("entities", [])
        logger.debug(f"✅ Loaded {len(entity_defs)} entities")

        # Step 2: Create folder structure
        if not resume or 'folders_created' not in state:
            create_java_structure(output_dir, application_name, logger)
            state['folders_created'] = True
            save_state(state_file, state)

        # 🔜 TODO: Step 3+ Entity/repo/service/controller gen

        logger.info("✅ Java backend generation completed!")

    except Exception as e:
        logger.error("❌ Generation failed: %s", str(e))
        handle_failure(str(e))
        rollback(project_name)


def create_java_structure(base_path, application_name, logger):
    """
    Create standard Spring Boot folder structure using:
    com/ashbyte/{applicationName}
    """
    base_dir = Path(base_path) / application_name / "src" / "main" / "java" / "com" / "ashbyte" / application_name

    folders = [
        "controller",
        "service",
        "service/impl",
        "repository",
        "model",
        "dto",
        "exception",
        "config"
    ]

    for folder in folders:
        path = base_dir / folder
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"📁 Created directory: {path}")

    # Also create test folders
    test_base = Path(base_path) / application_name / "src" / "test" / "java" / "com" / "ashbyte" / application_name
    for folder in ["controller", "service", "repository", "exception"]:
        path = test_base / folder
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"🧪 Created test directory: {path}")

    # Resources folder for application.yml, schema.sql etc.
    resources_dir = Path(base_path) / application_name / "src" / "main" / "resources" / "db"
    resources_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"📦 Created resources directory: {resources_dir}")