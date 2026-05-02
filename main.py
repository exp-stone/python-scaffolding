import argparse
import json
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from example_worker import ExampleWorker

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "config.json"
LOG_PATH = ROOT / "log.txt"
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Python scaffolding application.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=CONFIG_PATH,
        help="Path to a JSON configuration file.",
    )
    parser.add_argument(
        "--log-level",
        choices=LOG_LEVELS,
        help="Override the configured logging level.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=LOG_PATH,
        help="Path for file logging.",
    )
    parser.add_argument(
        "--app-name",
        help="Override the configured application name.",
    )
    parser.add_argument(
        "--to-screen",
        dest="to_screen",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable or disable console logging.",
    )
    parser.add_argument(
        "--to-file",
        dest="to_file",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable or disable file logging.",
    )
    return parser.parse_args(argv)


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def configure_logging(
    level: str = "INFO",
    to_screen: bool = False,
    to_file: bool = True,
    log_path: Path = LOG_PATH,
) -> logging.Logger:
    logger = logging.getLogger("Starting...")
    logger.setLevel(level.upper())
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    if to_file:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_screen:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


def get_cli_value(args: argparse.Namespace, name: str, default: Any) -> Any:
    value = getattr(args, name)
    return default if value is None else value


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    config = load_config(args.config)
    log_cfg = config.get("logging", {})
    app_cfg = config.get("app", {})
    app_name = get_cli_value(
        args, "app_name", app_cfg.get("name", "Python Scaffolding")
    )
    logger = configure_logging(
        level=get_cli_value(args, "log_level", log_cfg.get("level", "INFO")),
        to_screen=get_cli_value(args, "to_screen", log_cfg.get("to_screen", False)),
        to_file=get_cli_value(args, "to_file", log_cfg.get("to_file", True)),
        log_path=args.log_file,
    )

    logger.info("Starting %s", app_name)
    logger.debug("Loaded config: %s", config)
    ExampleWorker(logger).run()
    logger.info("Finished.")


if __name__ == "__main__":
    main()
