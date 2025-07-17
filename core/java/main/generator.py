# core/java/main/generator.py

import os
import json
import yaml
from pathlib import Path
from utils.logger import get_logger
from utils.error_handler import handle_failure, rollback, save_state, load_state
from core.java.project_files.dockerfile_generator import generate_docker_files
# (Import other generators as needed)

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
        project_path = Path(output_dir) / application_name
        if not resume or 'folders_created' not in state:
            create_java_structure(output_dir, application_name, logger)
            state['folders_created'] = True
            save_state(state_file, state)

        # Step 3: Generate Docker-related files
        if not resume or 'docker_created' not in state:
            generate_docker_files(project_path, logger)
            state['docker_created'] = True
            save_state(state_file, state)

        # 🔜 Add entity/service/repo/controller generation here

        logger.info("✅ Java backend generation completed!")

    except Exception as e:
        logger.error("❌ Generation failed: %s", str(e))
        handle_failure(str(e))
        rollback(project_name)


def create_java_structure(base_path, application_name, logger):
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

    test_base = Path(base_path) / application_name / "src" / "test" / "java" / "com" / "ashbyte" / application_name
    for folder in ["controller", "service", "repository", "exception"]:
        path = test_base / folder
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"🧪 Created test directory: {path}")

    resources_dir = Path(base_path) / application_name / "src" / "main" / "resources" / "db"
    resources_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"📦 Created resources directory: {resources_dir}")