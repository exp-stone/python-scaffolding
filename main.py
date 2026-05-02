import json
import logging
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "config.json"
LOG_PATH = ROOT / "log.txt"


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def configure_logging(
    level: str = "INFO", to_screen: bool = False, to_file: bool = True
) -> logging.Logger:
    logger = logging.getLogger("Starting...")
    logger.setLevel(level.upper())
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    if to_file:
        file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_screen:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


def main() -> None:
    config = load_config()
    log_cfg = config.get("logging", {})
    logger = configure_logging(
        level=log_cfg.get("level", "INFO"),
        to_screen=log_cfg.get("to_screen", False),
        to_file=log_cfg.get("to_file", True),
    )

    logger.info("starting ptest")
    logger.debug("loaded config: %s", config)
    logger.info("Finished.")


if __name__ == "__main__":
    main()
