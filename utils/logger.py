import logging
from pathlib import Path

def get_logger(name: str, project_name: str = None, version: str = None) -> logging.Logger:
    logs_path = Path("logs")
    logs_path.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    ch.setFormatter(ch_formatter)

    # File name based on project and version
    if project_name and version:
        log_filename = f"ashgenapp-{project_name}-{version}.log"
    else:
        log_filename = "genapp.log"

    log_file_path = logs_path / log_filename

    # File Handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(fh_formatter)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger